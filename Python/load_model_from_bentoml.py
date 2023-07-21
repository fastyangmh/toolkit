#import
import bentoml


#def
def load_model_from_bentoml(tag, **kwargs):
    loader = eval(bentoml.models.get(tag).info.module)
    model = loader.load_model(tag, **kwargs)
    return model


if __name__ == '__main__':
    #parameters
    tag = 'picklable_model_demo:hohbaqus5g6izlg6'

    #load model
    model = load_model_from_bentoml(tag=tag)
    print(model)