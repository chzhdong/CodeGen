# QHistory

QHistory aims to develop a history expert leveraging LLMs based on [QAnything](https://github.com/netease-youdao/QAnything).
This repo is only used for self learning, without purposes for commercial business.

- [What is QAnything](#what-is-qanything)
  - [Key features](#key-features)
  - [Architecture](#architecture)
- [Latest Updates](#-latest-updates)
- [Before You Start](#before-you-start)
- [Getting Started](#getting-started)
  - [Latest Features Table](#latest-features-table)
  - [Version 2.0.0 adds detailed optimizations:](#version-200-adds-detailed-optimizations)
    - [Display of data at each stage:](#display-of-data-at-each-stage)
    - [Problem fixed](#problem-fixed)
  - [Comparison of New and Old Parsing Effects](#comparison-of-new-and-old-parsing-effects)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [step1: pull qanything repository](#step1-pull-qanything-repository)
    - [step2: Enter the project root directory and execute the startup command.](#step2-enter-the-project-root-directory-and-execute-the-startup-command)
    - [step3: start to experience](#step3-start-to-experience)
    - [API](#api)
    - [DEBUG](#debug)
    - [Close service](#close-service)
  - [Offline Use](#offline-use)
  - [FAQ](#faq)
  - [Contributing](#contributing)
    - [Thanks to all contributors for their efforts](#thanks-to-all-contributors-for-their-efforts)
    - [Special thanks!](#special-thanks)
  - [Business contact information：](#business-contact-information)
- [Roadmap & Feedback](#-roadmap--feedback)
- [Community & Support](#community--support)
- [License](#license)
- [Acknowledgements](#acknowledgments)

## Key features

- Data security, supports installation and use by unplugging the network cable throughout the process. 
- Supports multiple file types, high parsing success rate, supports cross-language question and answer, freely switches between Chinese and English question and answer, regardless of the language of the file.
- Supports massive data question and answer, two-stage vector sorting, solves the problem of degradation of large-scale data retrieval, the more data, the better the effect, no limit on the number of uploaded files, fast retrieval speed. 
- Hardware friendly, defaults to running in a pure CPU environment, and supports multiple platforms such as Windows, Mac, and Linux, with no dependencies other than Docker. 
- User-friendly, no need for cumbersome configuration, one-click installation and deployment, ready to use, each dependent component (PDF parsing, OCR, embed, rerank, etc.) is completely independent, supports free replacement. 
- Supports a quick start mode similar to Kimi, fileless chat mode, retrieval mode only, custom Bot mode.

# Before You Start
**Star us on GitHub, and be instantly notified for new release!**
![star_us](https://github.com/netease-youdao/QAnything/assets/29041332/fd5e5926-b9b2-4675-9f60-6cdcaca18e14)
* [🏄 Try QAnything Online](https://qanything.ai)
* [📚 Try read.youdao.com | 有道速读](https://read.youdao.com)
* [🛠️ Only use our BCEmbedding(embedding & rerank)](https://github.com/netease-youdao/BCEmbedding)
* [📖 FAQ](FAQ_zh.md)
* [👂️Let me hear your voice](https://qanything.canny.io/feature-requests)

# Getting Started

## Installation
### Prerequisites
| **System** | **Required item**       | **Minimum Requirement** | **Note**                                                                               |
|------------|-------------------------|-------------------------|----------------------------------------------------------------------------------------|
|            | RAM Memory              | >= 20GB                 |                                                                                        |
| Linux/Mac  | Docker version          | >= 20.10.5              | [Docker install](https://docs.docker.com/engine/install/)                              |
| Linux/Mac  | docker compose  version | >= 2.23.3               | [docker compose install](https://docs.docker.com/compose/install/)                     |
| Windows    | Docker Desktop          | >= 4.26.1               | [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) |

### step1: pull qanything repository
```shell
git clone https://github.com/netease-youdao/QAnything.git
```
### step2: Enter the project root directory and execute the startup command.
* Execute the docker compose start command
* **The startup process takes about 30 seconds. When the log outputs "qanything backend service is ready!", the startup is complete!** 
```shell
cd QAnything
# Start on Linux
docker compose -f docker-compose-linux.yaml up
# Start on Mac
docker compose -f docker-compose-mac.yaml up
# Start on Windows
docker compose -f docker-compose-win.yaml up
```

(Note) If the startup fails, you can try changing `docker compose` to `docker-compose`.

### step3: start to experience
#### Front end
After successful installation, you can experience the application by entering the following addresses in your web browser.

- Front end address: http://localhost:8777/qanything/

### API
If you want to visit API, please refer to the following address:
- API address: http://localhost:8777/qanything/
- For detailed API documentation, please refer to [QAnything API documentation](docs/API.md)

### DEBUG
If you want to view the relevant logs, please check the log files in the `QAnything/logs/debug_logs` directory.
- **debug.log**
  - User request processing log
- **sanic_api.log**
  - Backend service running log
- **llm_embed_rerank_tritonserver.log**(Single card deployment)
  - LLM embedding and rerank tritonserver service startup log
- **llm_tritonserver.log**(Multi-card deployment)
  - LLM tritonserver service startup log
- **embed_rerank_tritonserver.log**(Multi-card deployment or use of the OpenAI interface.)
  - Embedding and rerank tritonserver service startup log
- rerank_server.log
  - Rerank service running log
- ocr_server.log
  - OCR service running log
- npm_server.log
  - Front-end service running log 
- llm_server_entrypoint.log
  - LLM intermediate server running log
- fastchat_logs/*.log
  - FastChat service running log

### Close service
```shell
# Front desk service startup mode like:
docker compose -f docker-compose-xxx.yaml up  # To close the service, please press Ctrl+C.
# Backend service startup mode like: 
docker compose -f docker-compose-xxx.yaml up -d # To close the service, please execute the following command.
docker compose -f docker-compose-xxx.yaml down
```

## Offline Use
If you want to use QAnything offline, you need to deploy the local large model (recommended to use ollama) on the offline machine in advance, and then you can start the service using the following command.
### Install offline for windows 
```shell
# Download the docker image on a networked machine
docker pull quay.io/coreos/etcd:v3.5.5
docker pull minio/minio:RELEASE.2023-03-20T20-16-18Z
docker pull milvusdb/milvus:v2.4.8
docker pull mysql:8.4
docker pull xixihahaliu01/qanything-win:v1.5.1  # From [https://github.com/netease-youdao/QAnything/blob/master/docker-compose-windows.yaml#L103] Get the latest version number.

# pack image
docker save quay.io/coreos/etcd:v3.5.5 minio/minio:RELEASE.2023-03-20T20-16-18Z milvusdb/milvus:v2.4.8 mysql:8.4 xixihahaliu01/qanything-win:v1.5.1 -o qanything_offline.tar

# download QAnything code
wget https://github.com/netease-youdao/QAnything/archive/refs/heads/master.zip

# Copy the image qanything_offline.tar and the code qany-master.zip to the offline machine 
cp QAnything-master.zip qanything_offline.tar /path/to/your/offline/machine

# Load image on offline machine 
docker load -i qanything_offline.tar

# Unzip the code and run it
unzip QAnything-master.zip
cd QAnything-master
docker compose -f docker-compose-win.yaml up
``` 
Similarly for other systems, just replace the corresponding image of the system, such as replacing mac with docker-compose-mac.yaml, and linux with docker-compose-linux.yaml
