pipeline {
  agent {
    node {
      label '172.22.27.211_Automation'
    }

  }
  stages {
    stage('run hello_world.py') {
      steps {
        sh '''
            ls -al
            python hello_world.py
        '''
      }
    }

  }
}