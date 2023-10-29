import pickle
# import torch
from haystack.pipelines import ExtractiveQAPipeline


def get_response(query):
    with open("app/nlp_engine/pickle/dbert.pkl", "rb") as model_file:
        # pipeline_components = torch.load(model_file, map_location=torch.device('cpu'), weights_only=False)
        # pipeline_components = {}
        # torch.save(pipeline_components, model_file)

        pipeline_components = pickle.load(model_file)
        retriever = pipeline_components["retriever"]
        reader = pipeline_components["reader"]

        pipe = ExtractiveQAPipeline(reader, retriever)

        prediction = pipe.run(
            query=query, params={"Retriever": {"top_k": 2}, "Reader": {"top_k": 5}}
        )

        pre_dict = prediction

        answers_list = pre_dict["answers"]

        answers_as_dict_list = []

        for answer in answers_list:
            answer_dict = {"answer": answer.answer}
            answers_as_dict_list.append(answer_dict)

        result = answers_as_dict_list[0]["answer"]
        return result
    
def get_response_roberta(query):
    with open("app/nlp_engine/pickle/roberta.pkl", "rb") as model_file:
        pipeline_components = pickle.load(model_file)
        retriever = pipeline_components["retriever"]
        reader = pipeline_components["reader"]

        pipe = ExtractiveQAPipeline(reader, retriever)

        prediction = pipe.run(
            query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
        )

        pre_dict = prediction

        answers_list = pre_dict["answers"]

        answers_as_dict_list = []

        for answer in answers_list:
            answer_dict = {"answer": answer.answer}
            answers_as_dict_list.append(answer_dict)

        result = answers_as_dict_list[0]["answer"]
        return result
