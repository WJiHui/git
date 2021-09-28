# 分支查看
### 查看所有分支
    git branch -a
### 查看本地分支与远程分支之间的追踪关系
    git branch -vv


# 分支建立
### 建立新分支
    git checkout -b new_branch
### 切换到某个分支
    git checkout new_branch
### 本地新建一个追踪远程分支的分支
    git checkout --track origin/branch
    git checkout -b branch origin/branch
### 本地已有一个分支，去追踪远程分支
    git branch --set-upstream-to=origin/<branch> local_branch
    
    

# 分支删除
### 删除一个本地分支
    git branch -d branch
### 删除远程分支
    远端分支已经删除，但是本地git branch -a 依然显示，使用命令 git push -p (prune)清除远端分支
    删除远程分支 ：git push [远程名] :[分支名] 
    在服务器上删除 serverfix 分支:  git push origin :serverfix    

# 拉取分支
### 从远程拉取分支，合并到本地分支
    git pull origin/branch <branch>
    git checkout -b 本地分支名x origin/远程分支名x