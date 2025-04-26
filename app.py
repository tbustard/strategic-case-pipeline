"""Command-line interface for case analysis."""

import click
from pathlib import Path
from case_context.assemble import assemble_answer

@click.command()
@click.argument('case_file', type=click.Path(exists=True))
@click.argument('question_file', type=click.Path(exists=True))
def main(case_file: str, question_file: str) -> None:
    """Analyze a case and answer a question about it.
    
    Args:
        case_file: Path to the case text file
        question_file: Path to the question text file
    """
    # Read input files
    case_text = Path(case_file).read_text()
    question_text = Path(question_file).read_text()
    
    # Get assembled answer
    answer = assemble_answer(case_text, question_text)
    
    # Print results
    click.echo("\nAnalysis Results:")
    click.echo("----------------")
    click.echo(answer)

if __name__ == "__main__":
    main() 