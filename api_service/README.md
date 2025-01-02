
## Prerequisites

Download and install the following:
* [Docker Desktop](https://docs.docker.com/desktop/)
* [Git Tool](https://git-scm.com/downloads)

## **Project Setup**

* Clone the JARVIS Repository in your desired local directory by opening cmd in the local folder & running the below command:
    * `git clone https://git.navis-dev.com/scm/hac24/jarvis.git`
* Open command line and change directory to `api_service`.
   * `cd api_service`
* Use the following command to start the service
   * `docker-compose -f docker-compose.yaml up -d`
* Use the following command to stop the service
  * `docker-compose -f docker-composer.yaml down`

## **Configuration**
* Open the file [admin.env](env_vars/admin.env)
* Check the table below to know more about the variables and set values to them according to your requirement
  
  * | Environment Variable           | Usage                                                                                                                                  |     Supported values |
    |:-------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------|---------------------:|
    | `HIDE_PII`                     | Whether to hide the Personal Identity Information in the input data. (Default: `True`)                                                 |       `True`/`False` |
    | `REPLACE_PII_WITH_FAKE_DATA`   | Whether to replace the Personal Identity Information with randomly generated fake data. (Default: `False`)                             |       `True`/`False` |
    | `USE_CHAT_HISTORY_IN_CONTEXT`  | Whether to contextualize the conversation/chat history and use it while generated answers for subsequent questions. (Default: `False`) |       `True`/`False` |

## **Note**

* The service is designed to download and store the necessary model files automatically during the initial startup. The first download may take some time due to the large size of the models.
* Please be patient while the models are being downloaded; the service will start once the download is complete.
* This happens only during the first startup of the service.

* Enabling `USE_CHAT_HISTORY_IN_CONTEXT` will utilize the conversation's context to generate answers, but it may result in slightly longer response times.
* Please checkout the postman collection and the environment attached in the sharepoint directory to test the APIs