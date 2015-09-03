'use strict';

const React = require('react');

const QuestionList = require('./question-list.jsx');

const Actions = require('./actions.js');
const Views = require('./views.js');

class Parse extends React.Component {
  formulaActive(formula) {
    this.props.dispatcher.dispatch({
      actionType: Actions.FORMULA_ACTIVE,
      formula: formula
    });
  }
  formulaInactive() {
    this.props.dispatcher.dispatch({
      actionType: Actions.FORMULA_INACTIVE
    });
  }
  formulaList(formulas) {
    const listItems = formulas.map((formula, i) => {
      const classes = [
        'flex-row',
        formula.isAligned ? 'is-aligned' : undefined,
        this.props.activeFormula && this.props.activeFormula.simple === formula.simple ? 'is-active' : undefined
      ].join(' ').trim();
      return (
        <li key={i}
            className={classes}
            onMouseEnter={this.formulaActive.bind(this, formula)}
            onMouseLeave={this.formulaInactive.bind(this)}>
          {formula.simple}: <em className="flex-right">{Math.round(formula.score * 100) / 100}</em>
        </li>
      );
    });
    return <ul className="formula-list">{listItems}</ul>;
  }
  advance() {
    this.props.dispatcher.dispatch({
      actionType: Actions.CHANGE_VIEW,
      view: Views.VIEW_OPTIMIZED_FORMULAS
    });
  }
  render() {
    return (
      <div className="flex-column flex-grow">
        <div className="flex-column flex-grow scrollable">
          <QuestionList
              questions={this.props.questions}
              dispatcher={this.props.dispatcher}
              selectedIndex={this.props.selectedIndex}
              selectedAnswerKey={this.props.solution ? this.props.solution.answer : undefined} />
          <div className="parsed-formulas flex-row">
            <div className="formula-list-container padded">
              <h2>Formulas Extracted from the Question Text:</h2>
              {this.formulaList(this.props.solution.textFormulas)}
            </div>
            <div className="formula-list-container padded">
              <h2>Formulas extracted from the Diagram:</h2>
              {this.formulaList(this.props.solution.diagramFormulas)}
            </div>
          </div>
        </div>
        <footer className="flex-row padded">
          <div className="instructions">GeoS extracted the formulas above.  Hover over each for more information.</div>
          <button className="flex-right" onClick={this.advance.bind(this)}>Next</button>
        </footer>
      </div>
    );
  }
}

module.exports = Parse;
