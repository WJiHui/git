## Reset
    --soft  缓存区和工作目录都不会改变
    --mixed 默认选项。 缓存区和你指定的提交同步，但工作目录不受影响
    --hard  缓存区和工作目录都同步到你指定的提交  

### 默认参数 --mixed
    将你当前的改动从缓存区中移除，但是这些改动还留在工作目录中，也就是取消提交，但本地保存修改
     git reset –mixed
     
### 撤销上一个commit,修改的代码依旧保留
    git reset --soft HEAD^ 
    git reset --soft HEAD^1
    
### 撤销commit,还原到上一个或者某个commit的原始状态,修改的代码不保留
    完全舍弃你没有提交的改动 ，也就是这个修改完全不要了，本地也不要了 
    git reset --hard HEAD^1/commit_id 
    如果用这个命令误删了，可以使用git relog查看，然后git reset –hard 1234567

### 取消所有修改，还原到某个远程分支的原始状态
     git reset --hard origin/branch_xxx
     git reset --hard FETCH_HEAD  放弃本地的文件修改，上一次成功git pull之后形成的commit点
     
### 回退两个提交
    git reset HEAD~2
     
