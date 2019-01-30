def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from cli.blog.cli import cli
if __name__ == "__main__":
    cli()