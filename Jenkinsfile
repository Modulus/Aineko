// this guarantees the node will use this template
def label = "mypod-${UUID.randomUUID().toString()}"
podTemplate(label: label, containers : [
    containerTemplate( name: "builder", image: "ubuntu:16.04", ttyEnabled: true),
    containerTemplate( name: "docker", image: "docker", command: "cat", ttyEnabled: true)
    ],
    volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]) {
    node(label) {
        def scmVars = checkout scm
        def gitCommit = env['GIT_COMMIT']
        def shortGitCommit = gitCommit[0..6]
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
                sh "echo 'aineko:1.${env.BRANCH_NAME}-${scmVars.GIT_COMMIT }'"
                sh "echo 'git commit: ${gitCommit}'
                sh "echo 'git shortCommit: ${shortGitCommit}'

               // sh "docker build --name aineko ."
            }
        }

    }
}