Motives: https://confluence.hrs.io/display/DEV/Githooks

# A useful set of git hooks to be used in dart/flutter project

The repository structure should follow documentation from [this package](https://pub.dev/packages/remote_hooks)

Hooks file to be executed has to follow the convention of
[the official git document](https://git-scm.com/book/fa/v2/Customizing-Git-Git-Hooks), although file extension
omitting is support by the hooks management package when perform installing, adding execution path at the top of
new hooks is crucial:

```shell
#!/usr/bin/env python3
```

There shouldn't be limitation on the programming language used to develop hooks, we can also use `dart`, in such case, 
the shebang become:

```shell
#!/usr/bin/env dart
```

Execution of hooks can be bypassed by adding `--no-verify` flag to the git command
```shell
$ git commit -m "message" --no-verify
```