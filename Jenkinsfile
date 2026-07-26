pipeline {
    agent any

    environment {
        // 切换环境：dev / test / prod
        TEST_ENV = "${params.ENV}"
        // CI 环境使用 headless 模式
        TEST_HEADLESS = 'true'
        // 浏览器类型
        TEST_BROWSER = 'chrome'
    }

    parameters {
        choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: '选择测试环境')
        choice(name: 'SCOPE', choices: ['all', 'ui', 'api'], description: '选择测试范围')
        string(name: 'MARKERS', defaultValue: '', description: '自定义 pytest markers，如 smoke 或 regression')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            when {
                anyOf {
                    expression { params.SCOPE == 'all' }
                    expression { params.SCOPE == 'api' }
                }
            }
            steps {
                bat '''
                    pytest tests/api/ -m api --alluredir=allure-results --clean-alluredir
                '''
            }
        }

        stage('Run UI Tests') {
            when {
                anyOf {
                    expression { params.SCOPE == 'all' }
                    expression { params.SCOPE == 'ui' }
                }
            }
            steps {
                bat '''
                    pytest tests/ui/ -m ui --alluredir=allure-results --clean-alluredir
                '''
            }
        }

        stage('Run by Markers') {
            when {
                expression { params.MARKERS != '' }
            }
            steps {
                bat """
                    pytest -m ${params.MARKERS} --alluredir=allure-results --clean-alluredir
                """
            }
        }
    }

    post {
        always {
            // 生成 Allure 报告
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]

            // 清理工作区
            cleanWs()
        }
        failure {
            echo 'Pipeline 执行失败，请检查日志和 Allure 报告'
        }
    }
}
