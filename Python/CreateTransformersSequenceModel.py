# import
import pandas as pd
import transformers
import torch.nn as nn

# class


class CreateTransformersSequenceModel:
    def __init__(self) -> None:
        self._get_content_from_url()

    def _get_content_from_url(self):
        url = 'https://huggingface.co/transformers/pretrained_models.html'
        self.content = pd.read_html(url)[0]

    def list_models(self, architecture=None):
        if architecture is None:
            return list(self.content['Model id'])
        else:
            return list(self.content['Model id'][self.content['Architecture'].str.lower() == architecture.lower()])

    def create_model(self, model_id, num_classes):
        if model_id in self.content['Model id'].values:
            architecture, model_id, detail = self.content[self.content['Model id']
                                                          == model_id].values[0]
            print(detail)
            model_class_name = [v for v in dir(transformers) if '{}ForSequenceClassification'.format(
                architecture).lower() == v.lower()]
            assert model_class_name, 'the model_id does not apply to sequence classification. the model_id is {}'.format(
                model_id)
            tokenizer_class_name = [v for v in dir(transformers) if v.lower(
            ).startswith('{}Tokenizer'.format(architecture).lower())][-1]
            tokenizer = eval('transformers.{}.from_pretrained("{}")'.format(
                tokenizer_class_name, model_id))
            model = eval('transformers.{}.from_pretrained("{}")'.format(
                model_class_name[-1], model_id))
            if model.classifier.out_features != num_classes:
                model.classifier = nn.Linear(
                    in_features=model.classifier.in_features, out_features=num_classes)
            return tokenizer, model
        else:
            assert False, 'the model_id does not exist in pretrained models. the model_id is {}'.format(
                model_id)


if __name__ == '__main__':
    # parameters
    model_id = 'albert-base-v2'

    # create object
    obj = CreateTransformersSequenceModel()

    # create tokenizer and model by model_id
    tokenizer, model = obj.create_model(model_id=model_id, num_classes=10)

    # list models
    print(obj.list_models())
