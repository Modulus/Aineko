// this guarantees the node will use this template
def label = "mypod-${UUID.randomUUID().toString()}"
podTemplate(label: label, containers : [
    containerTemplate( name: "builder", image: "ubuntu:16.04", ttyEnabled: true)
    ]) {
    node(label) {
        stage('Run tests') {
            container("builder"){
                sh "echo 'Install packages"
                sh "apt update && apt install -y python3 python3-pip"
                sh "echo 'Installing requirements for python project'"
                sh "pip3 install -r requirements.txt"
                sh "echo 'Running tests'"
                sh "cd tests && pytest ."
                sh "echo 'DONE!'"
            }

        }

    }
}