export function replaceWithHighlightedVersion(
    statements: string[],
    highlights: string[],
): string[] {
    if (!highlights || highlights.length === 0) return statements;

    // Function to apply highlights to a statement
    function applyHighlights(statement: string): string {
        for (const highlighted of highlights) {
            if (highlighted === "") continue;

            const unhighlighted = highlighted.replace(/<\/?em>/g, "");
            const highlightedRegex = new RegExp(unhighlighted.trim(), "g");
            statement = statement.replace(highlightedRegex, () => highlighted);
        }
        return statement;
    }

    // Apply highlights to all statements
    const highlightedStatements = statements.map(applyHighlights);

    // Find the first statement that includes any highlighted text
    const firstMatchIndex = highlightedStatements.findIndex(statement =>
        highlights.some(_ => statement.includes('<em>'))
    );

    // Return the array starting from the first match, or the full array if no match is found
    return firstMatchIndex >= 0
        ? highlightedStatements.slice(firstMatchIndex)
        : statements;
}
