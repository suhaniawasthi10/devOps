# Git Homework

## Task 1: git commit -a -m

### Difference between `git commit -m` and `git commit -a -m`

`git commit -m` is used when we have already staged the changes using `git add`.

Example:

```bash
git add Git/notes.md
git commit -m "Add Git homework notes"
```

`git commit -a -m` stages and commits the changes to already tracked files in one command. It does not include new untracked files.

Example:

```bash
git commit -a -m "Update Git notes"
```

### Commits created on main

I created three commits on the `main` branch:

```bash
git log --oneline
```

Output:

```text
b5e7ffb Add third main commit
27e0524 Update Git notes
c9782f7 Add Git homework notes
```

The first commit used `git commit -m` because the file was new and had to be staged first. For the next commits, I used `git commit -a -m` since the file was already tracked.

---

## Task 2: Git Cherry-Pick

For this task, I created a new branch called `feature` and made two commits on it.

### Create feature branch

```bash
git checkout -b feature
```

### Commits on feature branch

```bash
git log --oneline
```

Output:

```text
ac19302 (HEAD -> feature) Add cherry-pick change
221c82a Add feature branch change
b5e7ffb (main) Add third main commit
27e0524 Update Git notes
c9782f7 Add Git homework notes
```

The commit I selected for cherry-picking was:

```text
ac19302 Add cherry-pick change
```

### Cherry-pick the commit into main

First, I switched back to `main`:

```bash
git checkout main
```

Then I ran:

```bash
git cherry-pick ac19302
```

There was a merge conflict in `Git/notes.md`, so I resolved the conflict by keeping the required changes from both branches.

After resolving it, I ran:

```bash
git add Git/notes.md
git cherry-pick --continue
```

The cherry-pick was completed successfully.

### Verify the cherry-pick

```bash
git log --oneline
```

Output:

```text
b45b08b (HEAD -> main) Add cherry-pick change
b5e7ffb Add third main commit
27e0524 Update Git notes
c9782f7 Add Git homework notes
```

The cherry-picked commit is now present on `main` as:

```text
b45b08b Add cherry-pick change
```

I also checked the file:

```bash
cat Git/notes.md
```

Output:

```text
# Git Homework
Learning Git commit commands
Third commit on main
First change on feature branch
This change will be cherry-picked
```

This confirmed that the changes from the selected commit were successfully brought into the `main` branch.

---

## What I Learned

- `git commit -m` requires changes to be staged first.
- `git commit -a -m` can stage and commit changes to already tracked files.
- `git log --oneline` is useful for quickly finding commit IDs.
- `git cherry-pick` allows a specific commit from another branch to be added to the current branch.
- Cherry-picking can sometimes cause conflicts that need to be resolved manually.