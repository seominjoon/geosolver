'use strict';

const React = require('react');
const superagent = require('superagent');
const Promise = require('promise');

function get(url) {
  return new Promise((resolve, reject) => {
    superagent.get(url).send().end((err, response) => {
      if (!err && response) {
        try {
          const parsedJson = JSON.parse(response.text);
          resolve(parsedJson);
        } catch(e) {
          reject(e);
        }
      } else {
        reject(err);
      }
    });
  });
}

const prefixes = [ 'Moz', 'Webkit', 'Ms', 'O' ];
function prefixed(prop, value) {
  var styles = {};
  [ prop ].concat(prefixes.map((prefix) => {
    const propertyName = prefix + prop.substr(0, 1).toUpperCase() + prop.substr(1);
    styles[propertyName] = value;
  }));
  return styles;
}

const requestFrame = (
  typeof window.requestAnimationFrame === 'function'
    ? window.requestAnimationFrame
    : (fn) => {
        setTimeout(fn, 1000 / 7);
      }
);

function scrollTo(pos, cb) {
  const maxScroll = document.body.scrollHeight - window.innerHeight;
  const doScroll = () => {
    const diff = Math.min(Math.abs(pos - document.body.scrollTop), 100);
    if (
      diff !== 0 && (
        (pos > document.body.scrollTop && document.body.scrollTop !== maxScroll) ||
        (pos < document.body.scrollTop && document.body.scrollTop !== 0)
      )
    ) {
      requestFrame(() => {
        if (pos < document.body.scrollTop) {
          document.body.scrollTop -= diff;
        } else {
          document.body.scrollTop += diff;
        }
        doScroll();
      });
    } else if (typeof cb === 'function') {
      cb();
    }
  };
  doScroll();
}

const LoadingIndicator = React.createClass({
  render() {
    const loadingHtml = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="50" height="50"><path opacity=".25" d="M16 0 A16 16 0 0 0 16 32 A16 16 0 0 0 16 0 M16 4 A12 12 0 0 1 16 28 A12 12 0 0 1 16 4"></path><path d="M16 0 A16 16 0 0 1 32 16 L28 16 A12 12 0 0 0 16 4z"><animateTransform attributeName="transform" type="rotate" from="0 16 16" to="360 16 16" dur="0.5s" repeatCount="indefinite"></animateTransform></path</svg>"';
    return <div className="loading"  dangerouslySetInnerHTML={{__html: loadingHtml }}></div>;
  }
});

const ChoiceList = React.createClass({
  render: function() {
    let choices = [];
    for (let key in this.props.choices) {
      if (this.props.choices.hasOwnProperty(key)) {
        choices.push(<li key={key}>({key}) {this.props.choices[key]}</li>);
      }
    }
    return <ul className="choice-list">{choices}</ul>;
  }
});

const FormulaList = React.createClass({
  render: function() {
    const formulas = (
      this.props.formulas.length > 0
        ? this.props.formulas.map(function (formula, index) {
            return <li key={index}>{formula.simple}: <em>{formula.score}</em></li>;
          })
        : <li className="empty">Empty</li>
    );
    return (
        <div className={this.props.className}>
          <h2>{this.props.title}:</h2>
          <p className="description">{this.props.description}</p>
          <ul className="formula-list">{formulas}</ul>
        </div>
    );
  }
});

const Answer = React.createClass({
  render: function() {
    return (
        <div className="answer section">
          <h2 className="flex-row">
            <span>Answer: {this.props.answer.answer}</span>
            <span className="flex-right icon-check"></span>
          </h2>
          <div className="solve-button">
            <button onClick={this.props.onAskAgain}>Ask Another</button>
          </div>
        </div>
    );
  }
});

const Demo = React.createClass({
  getInitialState: function() {
    return {
      initialLoading: true,
      displaySolution: false,
      solutionLoading: false,
      selectedQuestionIndex: 0,
      questionKey: this.props.defaultQuestionKey
    };
  },
  updateQuestion: function(questionKey) {
    this.setState({questionKey: questionKey});
  },
  loadAllQuestions() {
    get(this.props.baseUrl + "dirs.json").then((questionDirs) => {
      const promises = questionDirs.map((dir) => {
        return get(this.props.baseUrl + dir + "/question.json").then((question) => {
          question.key = dir;
          return question;
        });
      });
      Promise.all(promises).then((questions) => {
        this.setState({ initialLoading: false, questions: questions });
      });
    });
  },
  componentDidMount() {
    this.loadAllQuestions();
  },

  solveQuestion() {
    const start = Date.now();

    this.setState({ displaySolution: true, solutionLoading: true }, () => {
      scrollTo(React.findDOMNode(this.refs.solution).offsetTop);
    });

    const question = this.state.questions[this.state.selectedQuestionIndex];
    const questionUrl = this.props.baseUrl + question.key + "/";
    const tp = get(questionUrl + "text_parse.json").then((formulas) => {
      this.setState({ textFormulas: formulas });
    });
    const dp = get(questionUrl + "diagram_parse.json").then((formulas) => {
      this.setState({ diagramFormulas: formulas });
    });
    const op = get(questionUrl + "optimized.json").then((formulas) => {
      this.setState({ optimizedFormulas: formulas });
    });
    const ap = get(questionUrl + "answer.json").then((answer) => {
      this.setState({ answer: answer });
    });
    Promise.all([tp,dp,op, ap]).then(() => {
      // Simulated latency
      setTimeout(() => {
        this.setState({ solutionLoading: false });
      }, Math.max(0, Math.random() * 2000 - (Date.now() - start)));
    });
  },

  selectPrevQuestion() {
    const prev = Math.max(0, this.state.selectedQuestionIndex - 1);
    this.setState({ selectedQuestionIndex: prev });
  },

  selectNextQuestion() {
    const next = Math.min(this.state.questions.length - 1, this.state.selectedQuestionIndex + 1);
    this.setState({ selectedQuestionIndex: next });
  },

  render: function() {

    let contents;
    if (this.state.initialLoading) {
      contents = <LoadingIndicator />;
    } else {

      const questions = this.state.questions.map(q => {
        return (
          <li key={q.key}>
            <p><img src={this.props.baseUrl + q.key + "/diagram.png"} /></p>
            <p>{q.text}</p>
            <ChoiceList choices={q.choices} />
          </li>
        );
      });


      let solutionContents;
      if (this.state.displaySolution) {
        if (this.state.solutionLoading) {
          solutionContents = <div className="loading-solution" ref="solution"><LoadingIndicator /></div>;
        } else {
          const askAgain = () => {
            scrollTo(0, () => {
              this.setState({ displaySolution: false });
            });
          };
          solutionContents = (
            <div className="solution" ref="solution">
              <div className="extractions flex-row section">
                <FormulaList className="proof text-parse" title="Text Parse" description="The information extracted from the question text." formulas={this.state.textFormulas} />
                <FormulaList className="proof diagram-parse" title="Diagram Parse" description="The information extracted from diagram." formulas={this.state.diagramFormulas} />
              </div>
              <FormulaList className="proof section optimized" title="Solution" description="The information optimized over text and diagram." formulas={this.state.optimizedFormulas} />
              <Answer answer={this.state.answer} onAskAgain={askAgain} />
            </div>
          );
        }
      }

      const icon = (
        <svg viewBox="0 0 32 32" width="50" height="50">
          <path d="M23.129,16.001c0,0.475-0.182,0.951-0.545,1.312L9.498,30.4l-2.626-2.626l11.774-11.773L6.872,4.228l2.626-2.627 l13.086,13.088C22.947,15.05,23.129,15.525,23.129,16.001z" />
        </svg>
      );

      const hasNext = this.state.selectedQuestionIndex < this.state.questions.length - 1;
      const hasPrev = this.state.selectedQuestionIndex > 0;
      const transform = prefixed('transform', 'translate3d(' + (-100 * this.state.selectedQuestionIndex) + '%,0,0)');

      contents = (
        <section>
          <div className="intro section">
            <h2>The GeoSolver is an end-to-end geometric question solver.</h2>
          </div>
          <div className="section">
            <h2>Select a Question:</h2>
            <div className="question-list flex-row">
              <button className="btn-transparent prev-question" onClick={this.selectPrevQuestion} disabled={!hasPrev}>{icon}</button>
              <div className="question"><ul className="flex-row" style={transform}>{questions}</ul></div>
              <button className="btn-transparent next-question" onClick={this.selectNextQuestion} disabled={!hasNext}>{icon}</button>
            </div>
            <div className="solve-button">
              <button onClick={this.solveQuestion}>Solve</button>
            </div>
          </div>
          {solutionContents}
        </section>
      );
    }
    return (
      <div>
        <header className="padded flex-row">
          <div>
            <h1>GeoSolver Demo</h1>
          </div>
          <div className="provided-by flex-row">
            <a href="http://allenai.org" target="_blank"><img src="assets/images/ai2_logo.png" width="360" height="71" /></a>
            <a href="https://www.cs.washington.edu/" target="_blank"><img src="assets/images/uw.png" width="75" height="75" /></a>
          </div>
        </header>
        <main>
          {contents}
        </main>
      </div>
    );
  }
});

React.render(
    <Demo baseUrl="assets/" defaultQuestionKey="968" />,
    document.body
);
