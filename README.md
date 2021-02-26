-------
# 基础概念
    集中化的版本控制系统（Centralized Version Control Systems，简称 CVCS）
    分布式版本控制系统（Distributed Version Control System，简称 DVCS）
 


-------  
# git 配置
## 查询配置信息
    git config --global  use global config file 一般是用户目录下的配置
    git config --system  use system config file 一般是系统etc下的配置
    git config --local   use repository config file 一般是当前代码库的配置
    git config -l/--list 显示所有配置，包含上面三个


## 配置文件配置
    git config -e/--edit    默认打开local配置
    git config --global -e  编辑~/.gitconfig    
1. 添加用户
    ```
    [user]
        name=xxx
        email=xxx@xx
    ```
2. 定义一个提交的模板
    ```
    [commit]
        template=path/to/file
    ```

## 命令行直接配置：
    git config --global user.name "John Doe" 配置用户信息：
    git config --global core.editor "vim"    配置git的默认编辑器
 

-------
# git 忽略文件
    创建一个名为 .gitignore 的文件，列出要忽略的文件模式
* 忽略所有 .a 结尾的文件
    *.a 
* lib.a 除外
    !lib.a
* 仅仅忽略项目根目录下的 TODO 文件，不包括 subdir/TODO
    /TODO  
* 忽略 build/ 目录下的所有文件
    build/
* 忽略 doc/notes.txt 但不包括 doc/server/arch.txt
    doc/*.txt
* 忽略所有这些文件夹中所有的 *.txt 文件
    doc/**/*.txt    
