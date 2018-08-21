// this guarantees the node will use this template
def label = "mypod-${UUID.randomUUID().toString()}"
podTemplate(label: label, containers : [
    containerTemplate( name: "builder", image: "ubuntu:16.04", ttyEnabled: true),
    containerTemplate( name: "docker", image: "docker", command: "cat", ttyEnabled: true)
    ],
    volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]) {
    node(label) {
       def repo = checkout scm
       def gitCommit = repo.GIT_COMMIT
       def gitBranch = repo.GIT_BRANCH
       def versionNumber = gitCommit.substring(0,10)
       // stage('Run tests') {
         //   container("builder"){
           //     sh "echo 'Install packages'"
             //   sh "apt update && apt install -y python3 python3-pip"
               // sh "echo 'Installing requirements for python project'"e
               // sh "ls -la"
                //sh "pip3 install -r requirements.txt"
                //sh "echo 'Running tests'"
                //sh "cd tests && pytest ."
                //sh "echo 'DONE!'"
            //}
        //}

        stage("Build container"){
            container("docker"){
                docker.withRegistry("https://tv2norge-docker-test-local.jfrog.io", "artifactory"){
                    def builtImage = docker.build("coderpews/aineko:1.coderpews/aineko:1.${versionNumber}-${env.BRANCH_NAME}")   
                    builtImage.push()
                }
              
            }

        }

    }
}
