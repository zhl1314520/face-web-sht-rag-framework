/**
* 定义一条 Jenkins CI 自动化测试流水线
* Jenkins 拉代码 -> 安装依赖 -> 执行测试 -> 生成 Allure 报告 -> 清理工作区，全部自动化
* 即：git pull -> pip install -> pytest -> allure -> cleanup，全部自动化
*
    pipeline       → 整条流水线
    agent          → 谁来执行
    environment    → 环境变量
    parameters     → 用户执行时选择的参数
    stages         → 流水线的步骤
    when           → 这个步骤什么时候执行
    post           → 流水线结束后的处理
*/


pipeline {  // pipeline：声明流水线
    agent any       // Jenkins 可以选择任意一个可用的 Agent（执行节点）来运行这条 Pipeline，当 jenkins server 启动时，会有多个 agent，
                    // 这些 agent 可以是本地的，也可以是远程的，甚至可以是云端的，Jenkins 会根据配置选择一个可用的 agent 来执行流水线任务。

    parameters {
        choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: '选择测试环境')    // 下拉框，用户自己选
        choice(name: 'SCOPE', choices: ['all', 'ui', 'api'], description: '选择测试范围')     // 下拉框，用户自己选
        string(name: 'MARKERS', defaultValue: '', description: '自定义 pytest markers，如 smoke 或 regression')
    }
    environment {
        // 切换环境：dev / test / prod
        TEST_ENV = "${params.ENV}"      // params 是 Jenkins Pipeline 提供的固定参数对象
        // CI 环境使用 headless 模式（无浏览器窗口模式）
        TEST_HEADLESS = 'true'
        // 浏览器类型
        TEST_BROWSER = 'chrome'
    }

    stages {        // stage：声明流水线阶段
        // 从仓库拉代码
        stage('Checkout') {
            steps {
                checkout scm    // scm：jenkins 提供的 Source Code Management（源代码管理）工具，checkout scm 表示从 SCM 中检出代码
            }
        }

        // 安装依赖，建立阶段
        stage('Setup') {
            steps {下·
                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {    // 接口自动化阶段
            when {
                anyOf {     // 只少选择 1 个
                    expression { params.SCOPE == 'all' }
                    expression { params.SCOPE == 'api' }
                }
            }   // when 里面意思：只有 SCOPE 是 all 或 api 时，才执行这个 Stage
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
                expression { params.MARKERS != '' }     // 只要 MARKERS 不为空，就执行
            }
            steps {
                bat """
                    pytest -m ${params.MARKERS} --alluredir=allure-results --clean-alluredir
                """
            }
        }
    }

    post {      // post：所有 stages 执行结束以后，根据 Pipeline 状态执行一些后置操作
        always {
            // 生成 Allure 报告
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]

            // 清理工作区（即 clean workspace）
            cleanWs()
        }
        failure {   // 只有 Pipeline 最终失败时执行
            echo 'Pipeline 执行失败，请检查日志和 Allure 报告'
        }
    }
}
