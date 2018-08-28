// this guarantees the node will use this template
def label = "mypod-${UUID.randomUUID().toString()}"
podTemplate(label: label, containers : [
    containerTemplate( name: "builder", image: "rubblesnask/ubuntu_python3_pip3:18.04.1", ttyEnabled: true,
        envVars: [
            envVar(key: "ELASTICSEARCH_URL", value: "localhost:9200")
         ]),
    containerTemplate( name: "docker", image: "docker", command: "cat", ttyEnabled: true)
    ],
    volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]) {

    node(label) {
       def repo = checkout scm
       def gitCommit = repo.GIT_COMMIT
       def gitBranch = repo.GIT_BRANCH
       def versionNumber = gitCommit.substring(0,10)
        stage('Run tests') {
            container("builder"){
                sh "echo 'Install packages'"
                sh "apt update && apt install -y python3 python3-pip"
                sh "echo 'Installing requirements for python project'"
                sh "ls -la"
                sh "pip3 install -r requirements.txt"
                sh "echo 'Running tests'"
                sh "cd tests && pytest . --junit-xml=`pwd`/rubblesnask_aineko_1.${versionNumber}-${env.BRANCH_NAME}-report.xml"
                sh "echo 'DONE!'"
            }
        }
        stage("Junit reports"){
            junit 'tests/*report.xml'
         }

        stage("Build container"){
            container("docker"){
                docker.withRegistry("https://registry.hub.docker.com", "dockerhub"){
                    def builtImage = docker.build("rubblesnask/aineko:1.${versionNumber}-${env.BRANCH_NAME}")
                    builtImage.push()
                }
            }
        }
    }
}
