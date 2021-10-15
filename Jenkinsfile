pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
        stage('Test') {
            steps {
                dir ('lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('isse_lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/isse-lib.git"
                }
                dir ('isse_lib/lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('sftp_lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/sftp-lib.git"
                }
                dir ('sftp_lib/lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                sh """
                virtualenv test_env
                source test_env/bin/activate
                pip2 install mock==2.0.0 --user
                pip2 install paramiko==1.8.0 --user
                pip2 install pathlib2==2.3.0 --user
                pip2 install pycrypto==2.3 --user
                pip2 install scandir==1.5 --user
                pip2 install simplejson==2.0.9 --user
                ./test/unit/isse_guard_transfer/_process_item.py
                ./test/unit/isse_guard_transfer/_remove_files.py
                ./test/unit/isse_guard_transfer/_send.py
                ./test/unit/isse_guard_transfer/cleanup.py
                ./test/unit/isse_guard_transfer/help_message.py
                ./test/unit/isse_guard_transfer/initate_process.py
                ./test/unit/isse_guard_transfer/load_cfg.py
                ./test/unit/isse_guard_transfer/main.py
                ./test/unit/isse_guard_transfer/move_to_reviewed.py
                ./test/unit/isse_guard_transfer/process.py
                ./test/unit/isse_guard_transfer/process_files.py
                ./test/unit/isse_guard_transfer/process_images.py
                ./test/unit/isse_guard_transfer/process_media.py
                ./test/unit/isse_guard_transfer/process_zip.py
                ./test/unit/isse_guard_transfer/run_program.py
                ./test/unit/isse_guard_transfer/set_sftp_conn.py
                ./test/unit/isse_guard_transfer/transfer_file.py
                deactivate
                rm -rf test_env
                """
            }
        }
        stage('SonarQube analysis') {
            steps {
                sh './test/unit/sonarqube_code_coverage.sh'
                sh 'rm -rf lib'
                sh 'rm -rf isse_lib'
                sh 'rm -rf sftp_lib'
                script {
                    scannerHome = tool 'sonar-scanner';
                }
                withSonarQubeEnv('Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner -Dproject.settings=sonar-project.JACIDM.properties"
                }
            
            }
        }
        stage('Artifactory upload') {
            steps {
                script {
                    server = Artifactory.server('Artifactory')
                    server.credentialsId = 'art-svc-highpoint-dev'
                    uploadSpec = """{
                        "files": [
                            {
                                "pattern": "./*.py",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/isse-transfer/"
                            },
                            {
                                "pattern": "./*.txt",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/isse-transfer/"
                            },
                            {
                                "pattern": "./*.md",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/isse-transfer/"
                            },
                            {
                                "pattern": "*.TEMPLATE",
                                "recursive": true,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/isse-transfer/config/"
                            }
                        ]
                    }"""
                    server.upload(uploadSpec)
                }
            }
        }
    }
    post {
        always {
            cleanWs disableDeferredWipeout: true
        }
    }
}
