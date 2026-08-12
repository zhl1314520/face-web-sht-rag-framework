/**
* pipeline：定义一条 Jenkins CI 自动化测试流水线
* Jenkins 拉代码 -> 安装依赖 -> 执行测试 -> 生成 Allure 报告 -> 清理工作区，全部自动化
* 即：git pull -> pip install -> pytest -> allure -> cleanup，全部自动化
*
    这些“变量名”都是固定的语法，不是约定，不能改变
    pipeline       → 整条流水线
    agent          → 谁来执行
    environment    → 环境变量
    parameters     → 用户执行时选择的参数
    stages         → 流水线的步骤
    when           → 这个步骤什么时候执行
    post           → 流水线结束后的处理

Jenkinsfile 的核心是 Groovy DSL
Jenkinsfile 包含
    Groovy 基础, 语法就是 Groovy 语法
    Declarative Pipeline 语法
    Jenkins Pipeline 常用指令
    Windows/Linux 执行命令
*/


pipeline {  // pipeline：声明流水线
    agent any       // Jenkins 可以选择从"已经配置好的节点"里面选择一个可用的 Agent（执行节点）来运行这条 Pipeline
                    // 这些 agent 可以是本地的，也可以是远程的，甚至可以是云端的，Jenkins 会根据配置选择一个可用的 agent 来执行流水线任务。

    parameters {
        choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: 'Select test environment')    // 下拉框，用户自己选
        choice(name: 'SCOPE', choices: ['all', 'ui', 'api'], description: 'select test scope')     // 下拉框，用户自己选
        string(name: 'MARKERS', defaultValue: '', description: 'define pytest markers，example smoke or regression')
    }
    environment {
        // 切换环境：dev / test / prod
        TEST_ENV = "${params.ENV}"      // params 是 Jenkins Pipeline 提供的固定参数对象
        // CI 环境使用 headless 模式（无浏览器窗口模式）
        TEST_HEADLESS = 'true'
        // 浏览器类型
        TEST_BROWSER = 'chrome'
        TEST_MARKERS = "${params.MARKERS}"
    }

    stages {        // stages：声明流水线的阶段
        // 从仓库拉代码
        stage('Checkout') {
            steps {
                checkout scm    // scm：jenkins 提供的 Source Code Management（源代码管理）工具，checkout scm 表示从 SCM 中检出代码
            }
        }

        // 安装依赖，建立阶段, 使用项目虚拟环境安装依赖，.venv\\Scripts\\python.exe：省去了激活虚拟环境的步骤，但是效果相同，且 CI 时效果更好
        stage('Setup') {
            steps {
                powershell(
                 encoding: 'UTF-8',
                 script: '''
                    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
                    $OutputEncoding = [System.Text.Encoding]::UTF8
                    $env:PYTHONIOENCODING = 'utf-8'

                    if (-not (Test-Path ".venv")) {
                        python -m venv .venv
                    }

                    .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
                )
            }
        }

        stage('Run API Tests') {    // 接口自动化阶段
            when {
                allOf {
                    expression { params.MARKERS == '' }     // 有自定义 markers 时跳过，由 Run by Markers 阶段执行
                    anyOf {     // 至少选择 1 个
                        expression { params.SCOPE == 'all' }
                        expression { params.SCOPE == 'api' }
                    }
                }
            }
            steps {
                powershell(
                 encoding: 'UTF-8',
                 script: '''
                    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
                    $OutputEncoding = [System.Text.Encoding]::UTF8
                    $env:PYTHONIOENCODING = 'utf-8'

                    .venv\\Scripts\\python.exe -m pytest tests\\api\\ --alluredir=allure-results\\api
                '''
                )
            }
        }

        stage('Run UI Tests') {
            when {
                allOf {
                    expression { params.MARKERS == '' }     // 有自定义 markers 时跳过，由 Run by Markers 阶段执行
                    anyOf {
                        expression { params.SCOPE == 'all' }
                        expression { params.SCOPE == 'ui' }
                    }
                }
            }
            steps {
                powershell(
                    encoding: 'UTF-8',
                    script: '''
                    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
                    $OutputEncoding = [System.Text.Encoding]::UTF8
                    $env:PYTHONIOENCODING = 'utf-8'

                    .venv\\Scripts\\python.exe -m pytest tests\\ui\\ --alluredir=allure-results\\ui
                '''
                )
            }
        }

        stage('Run by Markers') {
            when {
                expression { params.MARKERS != '' }     // 只要 MARKERS 不为空，就执行
            }
            steps {
                powershell(
                    encoding: 'UTF-8',
                    script: '''
                    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
                    $OutputEncoding = [System.Text.Encoding]::UTF8
                    $env:PYTHONIOENCODING = 'utf-8'

                    .venv\\Scripts\\python.exe -m pytest -m ${params.MARKERS} --alluredir=allure-results\\markers
                '''
                )
            }
        }
    }

    post {      // post：所有 stages 执行结束以后，根据 Pipeline 状态执行一些后置操作
        always {
            // 用 Jenkins 生成 Allure 报告，当前写法是 allure2
            script {
                bat '''
                    echo ===== WHO AM I =====
                    whoami

                    echo ===== USERPROFILE =====
                    echo %USERPROFILE%

                    echo ===== JENKINS_HOME =====
                    echo %JENKINS_HOME%

                    echo ===== WORKSPACE =====
                    echo %WORKSPACE%

                    echo ===== ALLURE DIRECTORY =====
                    dir "%USERPROFILE%\\.jenkins\\tools\\org.allurereport.jenkins.tools.AllureCommandlineInstallation" /s /b 2>nul

                    echo ===== ALLURE BAT SEARCH =====
                    where /r "C:\\Users" allure.bat 2>nul
                '''
                if (fileExists('allure-results')) {
                    allure(
                        includeProperties: false,
                        jdk: '',
                        results: [
                            [path: 'allure-results']
                        ]
                    )
                } else {
                    echo '未找到 allure-results 目录，跳过 Allure 报告生成'
                }
            }
      // 清理工作区（即 clean workspace）
      cleanWs()
    }
    failure {   // 只有 Pipeline 最终失败时执行
            echo 'Pipeline 执行失败，请检查日志和 Allure 报告'
        }
    }
}
