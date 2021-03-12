## git stash  储藏
    git stash list  查看储藏  堆栈方式存储的
	git stash apply 或者 git stash apply stash@{X}
	git stash apply --index  重新应用被暂存的变更
	git stash pop   恢复储藏并且将其从堆栈中移走
	git stash drop stash@{0}  移除指定的储藏 stash
