App Evaluation Tool

For the evaluation of how well the application answers to the user's queries,
we have used the RAGAS framework to calculate the below mentioned metrics

1. Answer Relevance - Measures the relevance of the LLM's answer with the query
2. Context Precision - Measures the precision of the context with the ground_truth (annotated answer)
3. Faithfulness - Measures how faithful the answer was generated by the LLM pertinent to the context provided by the retriever.
4. Context Recall - measures the extent to which the retrieved context aligns with the ground_truth.


Guide Steps
1. Create a csv file named **test_dataset.csv** ( filename should be exactly same ) with the following columns
   1. query
   2. ground_truth
2. Please view the sample test_dataset.csv in data folder.
3. Start the backend service as specified in the api_service README file.
4. Configure the properties mentioned in the .env file.
   1. APP_SERVER_HOST - hostname of the server
   2. APP_SERVER_PORT - port of the server
   3. APP_OLLAMA_HOST - ollama server host
   4. APP_OLLAMA_PORT - ollama server port
   5. TOPIC - queries of the topic to be evaluated
   6. RAGAS_MODEL_FOR_EVAL - mention the model that you would like ragas to internally use for evaluation
5. docker compose up
6. After the evaluation is done, you can find your results in data/results.csv

Note:
1. Please make sure you have a good internet connection and sufficient data as different LLM models would need to be pulled during startup.
2. The model specified for the ragas evaluation will be pulled before the evaluation starts
3. The evaluation takes time.
4. Please checkout result.csv to view the results of how well the app has performed.

Reference:
1. https://docs.ragas.io/en/stable/concepts/metrics/index.html