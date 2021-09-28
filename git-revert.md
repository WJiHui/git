# revert与reset的区别
    revert是撤销某一个提交，不影响这个提交前后的提交
    reset是回退到某个提交，这个提交之后的提交都取消，所以一般用于最新提交的修改

# 使用
    git revert -n commit_id
    git status 查看，如果有冲突的文件，修改一下
    git commit

# 注意
    使用revert撤销是新提一个commit去修改原来的提交，所以git log依然会记录以前的提交，也就是依然会留下痕迹。
    使用git rebase修改，然后git push -f origin master(强制提交到远程的masetr分支)这样就是无痕修改。

