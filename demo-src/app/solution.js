'use strict';

const uniqueSortedFormulas = (formulas) => {
  const len = formulas.length;
  return formulas.filter((formula, index, arr) => {
    let i = 0;
    for(; i < len; i++) {
      if (arr[i].simple === formula.simple) {
        break;
      }
    }
    return i === index;
  }).sort((a, b) => b.score - a.score);
};

const withAlignments = (formulas, alignmentTargets) => {
  return formulas.map(formula => {
    formula.isAligned = alignmentTargets.some(target => target.simple === formula.simple);
    return formula;
  });
};

class QuestionSolution {
  constructor(question, textFormulas, diagramFormulas, optimizedFormulas, solutionFormula, answer) {
    const uniqueTextFormulas = uniqueSortedFormulas(textFormulas);
    const uniqueDiagramFormulas = uniqueSortedFormulas(diagramFormulas);
    this.question = question;
    this.textFormulas = withAlignments(uniqueTextFormulas, uniqueDiagramFormulas);
    this.diagramFormulas = withAlignments(uniqueDiagramFormulas, uniqueTextFormulas);
    this.optimizedFormulas = uniqueSortedFormulas(optimizedFormulas);
    this.solutionFormula = solutionFormula;
    this.answer = answer.answer;
  }
}

module.exports = QuestionSolution;
