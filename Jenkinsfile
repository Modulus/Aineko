// this guarantees the node will use this template
def label = "mypod-${UUID.randomUUID().toString()}"
podTemplate(label: label, containers : [
    containerTemplate( name: "builder", image: "ubuntu:16.04", ttyEnabled: true),
    containerTemplate( name: "docker", image: "docker", command: "cat", ttyEnabled: true)
    ],
    volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]) {
    node(label) {
        checkout scm
       // stage('Run tests') {
         //   container("builder"){
           //     sh "echo 'Install packages'"
             //   sh "apt update && apt install -y python3 python3-pip"
               // sh "echo 'Installing requirements for python project'"
               // sh "ls -la"
                //sh "pip3 install -r requirements.txt"
                //sh "echo 'Running tests'"
                //sh "cd tests && pytest ."
                //sh "echo 'DONE!'"
            //}
        //}
        stage("Build container"){
            container("docker"){
                sh "Building aineko:${env.BRANCH_NAME}${env.TAG_NAME}"
               // sh "docker build --name aineko ."
            }
        }

    }
}