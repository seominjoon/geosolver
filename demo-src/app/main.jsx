'use strict';

const React = require('react');
const Dispatcher = require('flux').Dispatcher;

const LoadingIndicator = require('./loading.jsx');
const SelectQuestion = require('./select-question.jsx');
const Parse = require('./parse.jsx');
const Optimized = require('./optimized.jsx');
const Solution = require('./solution.jsx');

const Actions = require('./actions.js');
const QuestionStore = require('./question-store.js');
const Views = require('./views.js');

class GeoSolverDemo extends React.Component {
  constructor(props) {
    super(props);
    this.dispatcher = new Dispatcher();
    this.questionStore = new QuestionStore(this.dispatcher);
    this.state = this.questionStore.state;
  }
  componentDidMount() {
    this.onQuestionStoreChange = (state) => {
      this.setState(state);
    };
    this.questionStore.addChangeListener(this.onQuestionStoreChange);
    this.dispatcher.dispatch({
      actionType: Actions.LOAD_QUESTIONS,
    });
  }
  componentWillUnmount() {
    this.questionStore.removeChangeListener(this.onQuestionStoreChange);
  }
  render() {
    let content;
    if (Array.isArray(this.state.questions)) {
      switch(this.state.activeView) {
        case Views.SELECT_QUESTIONS: {
          content = (
            <SelectQuestion
                {...this.state}
                dispatcher={this.dispatcher}
                questionStore={this.questionStore} />
          );
          break;
        }
        case Views.VIEW_PARSED_FORMULAS: {
          content = (
            <Parse
                {...this.state}
                dispatcher={this.dispatcher}
                questionStore={this.questionStore} />
          );
          break;
        }
        case Views.VIEW_OPTIMIZED_FORMULAS: {
          content = (
            <Optimized
                {...this.state}
                dispatcher={this.dispatcher}
                questionStore={this.questionStore} />
          );
          break;
        }
        case Views.VIEW_SOLUTION: {
          content = (
            <Solution
                {...this.state}
                dispatcher={this.dispatcher}
                questionStore={this.questionStore} />
          );
          break;
        }
      }
    } else {
      content = <LoadingIndicator />;
    }
    return (
      <div className="viewport flex-column">
        <header className="flex-row padded">
          <h1>GeoS Demo — An End to End Geometry Problem Solver</h1>
          <div className="flex-right flex-row provided-by">
            <a href="http://allenai.org" target="_blank"><img src="assets/images/ai2_logo.png" width="66" height="50" /></a>
            <a href="https://www.cs.washington.edu/" target="_blank"><img src="assets/images/uw.png" width="50" height="50" /></a>
          </div>
        </header>
        <main className="flex-column flex-grow">{content}</main>
      </div>
    );
  }
}

React.render(<GeoSolverDemo />, document.body);
