'use strict';

const React = require('react');

const QuestionList = require('./question-list.jsx');

const Actions = require('./actions.js');
const Views = require('./views.js');

class Optimized extends React.Component {
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
      view: Views.VIEW_SOLUTION
    });
  }
  goBack() {
    this.props.dispatcher.dispatch({
      actionType: Actions.CHANGE_VIEW,
      view: Views.VIEW_PARSED_FORMULAS
    });
  }
  render() {
    return (
      <div className="flex-column flex-grow not-scrollable">
        <div className="flex-column flex-grow not-scrollable">
          <QuestionList
              questions={this.props.questions}
              dispatcher={this.props.dispatcher}
              selectedIndex={this.props.selectedIndex}
              activeFormula={this.props.activeFormula}
              entityMap={this.props.solution.entityMap}
              selectedAnswerKey={this.props.solution ? this.props.solution.answer : undefined} />
          <div className="formula-list-container padded scrollable">
            <h2>Optimized List of Formulas:</h2>
            {this.formulaList(this.props.solution.optimizedFormulas)}
          </div>
        </div>
        <footer className="flex-row padded">
          <button className="btn-prev" onClick={this.goBack.bind(this)}>Previous</button>
          <div className="instructions">GeoS combined the extracted formulas into the optimized list shown above.</div>
          <button className="flex-right" onClick={this.advance.bind(this)}>Next</button>
        </footer>
      </div>
    );
  }
}

module.exports = Optimized;
