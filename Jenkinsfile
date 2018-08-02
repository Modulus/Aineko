// this guarantees the node will use this template
def label = "mypod-${UUID.randomUUID().toString()}"
podTemplate(label: label, containers : [
    containerTemplate( name: "python", image: "python:3.7.0-slim", ttyEnabled: true, command: "cat")
    ]) {
    node(label) {
        stage('Run tests') {
            sh "echo 'Installing requirements'"
            sh "pip install -r requirements.txt"
            sh "echo 'Running tests'"
            sh "cd tests && pytest ."
            sh "echo 'DONE!'"
        }

    }
}