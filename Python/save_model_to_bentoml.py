#import
import bentoml


#def
def save_model_to_bentoml(framework_name, name, model, signatures, labels,
                          custom_objects, external_modules, metadata):
    operator_table = {
        'pytorch': bentoml.pytorch.save_model,
        'picklable_model': bentoml.picklable_model.save_model,
        'onnx': bentoml.onnx.save_model,
    }

    operator = operator_table[framework_name]

    result = operator(name=name,
                      model=model,
                      signatures=signatures,
                      labels=labels,
                      custom_objects=custom_objects,
                      external_modules=external_modules,
                      metadata=metadata)

    return result


class Picklable_model:
    def __init__(self) -> None:
        pass

    def __call__(self, inputs):
        return inputs


if __name__ == '__main__':
    #parameters

    #initial model
    model = Picklable_model()

    #save to bentoml
    result = save_model_to_bentoml(framework_name='picklable_model',
                                   name='picklable_model',
                                   model=model,
                                   signatures=None,
                                   labels=None,
                                   custom_objects=None,
                                   external_modules=None,
                                   metadata=None)
    print(result)
