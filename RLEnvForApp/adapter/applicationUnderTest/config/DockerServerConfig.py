MAXIMUM_WAITING_TIMEOUT = 1000
DOCKER_IMAGE_CREATOR = "ntutselab"
APPLICATION_NAME = "Application"
PORT = "3000"


def dockerComposeFileName(applicationName: str, port: str):
    fileName = f"docker_compose_{applicationName}_{port}.yml"
    return fileName


def dockerComposeFileContent(dockerImageCreator: str = DOCKER_IMAGE_CREATOR, applicationName: str = APPLICATION_NAME,
                             port: str = PORT):
    if applicationName == "timeoff_management_with_coverage":
        return getTimeoffDockerComposeFile(port)

    if applicationName == "keystonejs_with_coverage":
        return getKeystoneJSDockerComposeFile(port)

    if applicationName == "nodebb_with_coverage":
        return getNodebbDockerComposeFile(port)

    if applicationName == "django_blog_with_no_coverage":
        return getDjangoBlogDockerComposeFile(port)

    if applicationName == "spring_petclinic_with_no_coverage":
        return getSpringPetclinicDockerComposeFile(port)

    if applicationName == "kimai":
        return getKimaiDockerComposeFile(port)

    if applicationName == "astuto":
        return getAstutoDockerComposeFile(port)

    if applicationName == "oscar":
        return getOscarDockerComposeFile(port)

    if applicationName == "svelte_commerce":
        return getSvelteCommerceDockerComposeFile(port)

    if applicationName == "mern_forum":
        return getMernForumDockerComposeFile(port)

    # compose_file_content = '{applicationName}_{port}:\n' \
    #                        ' image: {dockerImageCreator}/{applicationName}\n' \
    #                        ' ports:\n' \
    #                        '  - "{port}:3000"'
    #
    # if applicationName == "nodebb_with_coverage":
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:4567"\n' \
    #                            ' links:\n' \
    #                            '  - mongodb_{port}\n' \
    #                            ' environment:\n' \
    #                            '  - MONGO_HOST=mongodb_{port}\n' \
    #                            'mongodb_{port}:\n' \
    #                            ' image: ntutselab/mongo'
    #
    # if applicationName == "keystonejs_with_coverage":
    #     dbPort = 27000 + int(port) % 3000
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:3000"\n' \
    #                            ' links:\n' \
    #                            '  - nameOfMongoDB\n' \
    #                            ' environment:\n' \
    #                            '  - MONGO_URI=mongodb://nameOfMongoDB:27017/\n' \
    #                            'nameOfMongoDB:\n' \
    #                            ' image: mongo\n' \
    #                            ' ports:\n' \
    #                            '  - "' + str(dbPort) + ':27017"'
    #
    # if applicationName == "wagtails_with_coverage":
    #     dockerImageCreator = "ntuthongkaihuang"
    #     applicationName = "wagtail"
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:8000"'
    #
    # if applicationName == "django_blog_with_no_coverage":
    #     dockerImageCreator = "lidek213"
    #     applicationName = "django-blog_for_experiment"
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:3000"'
    # if applicationName == "spring_petclinic_with_no_coverage":
    #     dockerImageCreator = "lidek213"
    #     applicationName = "spring-petclinic_for_experiment"
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' command: java -jar /spring-petclinic/build/libs/spring-petclinic-2.6.0.jar /spring-petclinic/build/libs/spring-petclinic-2.6.0-plain.jar\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:8080"'
    #
    # compose_file_content = compose_file_content.format(dockerImageCreator=dockerImageCreator,
    #                                                    applicationName=applicationName, port=port)
    # return compose_file_content


def createDockerComposeCommand(dockerComposePath: str):
    return ["docker", "compose", "-f", dockerComposePath, "up", "-d", "--wait"]


def removeDockerComposeCommand(dockerComposePath: str):
    return ["docker", "compose", "-f", dockerComposePath, "rm", "-svf"]


def findDockerComposeContainerIdCommand(dockerComposePath: str):
    return ["docker", "compose", "-f", dockerComposePath, "ps", "-q"]


def getTimeoffDockerComposeFile(port: str = PORT):
    config = f'''
    services:
      timeoff_management_with_coverage_{port}:
        image: ntutselab/timeoff_management_with_coverage
        ports:
        - "{port}:3000"
        healthcheck:
          test: ["CMD", "wget", "--spider", "-q", "-S", "-O", "/dev/null", "http://localhost:3000/login/"]
          interval: 10s
          timeout: 5s
          retries: 10
          start_period: 280s
    '''
    return config


def getKeystoneJSDockerComposeFile(port: str = PORT):
    config = f'''
    services:
      keystonejs_with_coverage_{port}:
        image: ntutselab/keystonejs_with_coverage
        ports:
          - '{port}:3000'
        links:
          - nameOfMongoDB
        environment:
          - 'MONGO_URI=mongodb://nameOfMongoDB:27017/'
        healthcheck:
          test: ["CMD-SHELL", "node -e \\"require('http').request('http://localhost:3000/keystone', {{timeout: 3000}}, res => process.exit(res.statusCode < 400 ? 0 : 1)).on('error', () => process.exit(1)).end()\\""]
          interval: 2s
          timeout: 1s
          retries: 25
          start_period: 460s
        depends_on:
          nameOfMongoDB:
            condition: service_healthy
      nameOfMongoDB:
        image: ntutselab/mongo
        tmpfs:
          - /data/db
        ports:
          - '27001:27017'
        healthcheck:
          test: ["CMD-SHELL", "echo 'db.runCommand(\\"{{ ping: 1 }}\\").ok' | mongo localhost:27017/test --quiet"]
          interval: 2s
          timeout: 1s
          retries: 25
          start_period: 10s
    '''
    return config


def getNodebbDockerComposeFile(port: str = PORT):
    config = f'''
    services:
      nodebb_with_coverage_{port}:
        image: ntutselab/nodebb_with_coverage
        ports:
          - '{port}:4567'
        links:
          - mongodb_1
        environment:
          - MONGO_HOST=mongodb_1
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:4567"]
          interval: 2s
          timeout: 1s
          retries: 25
          start_period: 160s
        depends_on:
          mongodb_1:
            condition: service_healthy
      mongodb_1:
        image: ntutselab/mongo
        tmpfs:
          - /data/db
        healthcheck:
          test: ["CMD-SHELL", "echo 'db.runCommand(\\"{{ ping: 1 }}\\").ok' | mongo localhost:27017/test --quiet"]
          interval: 2s
          timeout: 1s
          retries: 25
          start_period: 10s
    '''
    return config


def getDjangoBlogDockerComposeFile(port: str = PORT):
    config = f'''
    services:
      django_blog_with_no_coverage_{port}:
        image: lidek213/django-blog_for_experiment
        ports:
          - "{port}:3000"
        healthcheck:
          test: ["CMD", "wget", "--spider", "-q", "-S", "-O", "/dev/null", "http://127.0.0.1:3000"]
          interval: 2s
          timeout: 1s
          retries: 25
          start_period: 280s
    '''
    return config


def getSpringPetclinicDockerComposeFile(port: str = PORT):
    config = f'''
    services:
      spring_petclinic_with_no_coverage_{port}:
        image: lidek213/spring-petclinic_for_experiment:latest
        command: java -jar /spring-petclinic/build/libs/spring-petclinic-2.6.0.jar /spring-petclinic/build/libs/spring-petclinic-2.6.0-plain.jar
        ports:
          - '{port}:8080'
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8080/"]
          interval: 2s
          timeout: 1s
          retries: 25
          start_period: 120s
    '''
    return config


def getKimaiDockerComposeFile(port: str = PORT):
    config = f'''
    version: '3.5'
    services:

      sqldb:
        image: mysql:5.7
        volumes:
          - kimai-mysql:/var/lib/mysql
        environment:
          - MYSQL_DATABASE=kimai
          - MYSQL_USER=kimaiuser
          - MYSQL_PASSWORD=kimaipassword
          - MYSQL_ROOT_PASSWORD=changemeplease
        command: --default-storage-engine innodb
        restart: unless-stopped
        healthcheck:
          test: mysqladmin -p$$MYSQL_ROOT_PASSWORD ping -h localhost
          interval: 20s
          start_period: 10s
          timeout: 10s
          retries: 3

      kimai_{port}:
        image: kimai/kimai2:apache
        volumes:
          - kimai-var:/opt/kimai/var
        ports:
          - {port}:8001
        environment:
          - ADMINMAIL=vector@selab.com
          - ADMINPASS=selab1623
          - DATABASE_URL=mysql://kimaiuser:kimaipassword@sqldb/kimai
          - TRUSTED_HOSTS=nginx,localhost,127.0.0.1
        restart: unless-stopped

    volumes:
      kimai-var:
      kimai-mysql:
    '''
    return config


def getAstutoDockerComposeFile(port: str = PORT):
    config = f'''
    version: '3.4'
    services:
      db:
        image: postgres:14.5
        environment:
          POSTGRES_USER: astuto
          POSTGRES_PASSWORD: dbpass
      astuto_{port}:
        image: riggraz/astuto
        environment:
          POSTGRES_USER: astuto
          POSTGRES_PASSWORD: dbpass
          BASE_URL: http://localhost:3000
          SECRET_KEY_BASE: secretkeybasehere
        ports:
          - "{port}:3000"
        depends_on:
          - db
    '''
    return config


def getOscarDockerComposeFile(port: str = PORT):
    config = f'''
    services:
      oscar:
        image: oscarcommerce/django-oscar-sandbox
        ports:
          - "{port}:8080"
    '''
    return config


def getSvelteCommerceDockerComposeFile(port: str = PORT):
    config = f'''
    version: '3.8'
    services:
      svelte-commerce:
        image: ghcr.io/itswadesh/svelte-commerce
        ports:
          - "{port}:3000"
    '''
    return config

def getMernForumDockerComposeFile(port: str = PORT):
    config = f'''
     services:
        mongo_db:
            image: mongo:latest
            restart: always
            networks:
                - network-db
        app_{port}:
            image: ntutselab/mern-forum-app:latest
            ports:
                - {port}:3000
                - 8001:8000
            environment:
                NODE_ENV: deveplopment
                PORT: 8000
                BACKEND: http://localhost:8001
                CLIENT: http://localhost:{port}
                REACT_APP_BACKEND_URL: http://localhost:8001
                MONGODB: mongodb://mongo_db:27017/MERN-Forum
                SECRET: ssOWR8CGLa
            depends_on:
                - mongo_db
            networks:
                - network-db
     networks:
        network-db:
    '''
    return config
