'use strict';

const React = require('react');
const superagent = require('superagent');
const Promise = require('promise');

var QuestionKeyList = React.createClass({
  onSubmit: function(e) {
    e.preventDefault();
    var questionKey = React.findDOMNode(this.refs.questionKey).value.trim();
    this.props.updateQuestion(questionKey);
    return;
  },
  render: function() {
    var questionNodes = this.props.questionKeys.map(function (questionKey) {
      return (
          <option questionKey={questionKey}>
            {questionKey}
          </option>
      );
    });
    return (
        <div className="questionList">
          <h2>Questions</h2>
          <form className="questionListForm" onSubmit={this.onSubmit}>
            <select ref="questionKey">
              {questionNodes}
            </select>
            <input type="submit" value="Go" />
          </form>
        </div>
    );
  }
});

var Choice = React.createClass({
  render: function() {
    return (
        <div className="choice">
          {this.props.myKey}: {this.props.myValue}
        </div>
    );
  }
});

var ChoiceList = React.createClass({
  render: function() {

    var choiceNodes = [];
    for (var key in this.props.choices) {
      if (this.props.choices.hasOwnProperty(key)) {
        choiceNodes.push(
            <Choice myKey={key} myValue={this.props.choices[key]} />
        );
      }
    }
    return (
        <div className="choiceList">
          {choiceNodes}
        </div>
    );
  }
});

var QuestionBox = React.createClass({
  render: function() {
    return (
        <div className="questionBox">
          <h2>Question</h2>
          <p>{this.props.question.text}</p>
          <img src={this.props.diagramUrl} />
        </div>
    );
  }
});

var Formula = React.createClass({
  render: function() {
    return (
        <div className="formula">
          {this.props.formula.simple}: {this.props.formula.score}
        </div>
    );
  }
});

var FormulaList = React.createClass({
  render: function() {
    var formulaNodes = this.props.formulas.map(function (formula, index) {
      return (
          <Formula key={index} formula={formula}/>
      );
    });
    return (
        <div className={this.props.className}>
          <h2>{this.props.title}</h2>
          {formulaNodes}
        </div>
    );
  }
});

var Answer = React.createClass({
  render: function() {
    return (
        <div className="answer">
          <h2>Answer</h2>
          <p>{this.props.answer}</p>
        </div>
    );
  }
});

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

var Demo = React.createClass({
  getInitialState: function() {
    return {
      initialLoading: true,
      displaySolution: false,
      solutionLoading: true,
      questionKey: this.props.defaultQuestionKey

    }
  },
  updateQuestion: function(questionKey) {
    this.setState({questionKey: questionKey});
  },
  loadAllQuestions() {
    get(this.props.baseUrl + "dirs.json").then((questionDirs) => {
      console.log(questionDirs);
      const promises = questionDirs.map((dir) => {
        return get(this.props.baseUrl + dir + "/question.json").then((question) => {
          question.key = dir;
          return question;
        });
      });
      Promise.all(promises).then((questions) => {
        console.log(questions);
        this.setState({ initialLoading: false, questions: questions });
      });
    })
  },
  componentDidMount() {
    this.loadAllQuestions();
  },

  solveQuestion(question) {
    this.setState({displaySolution: true});
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
    Promise.all([tp,dp,op]).then((promises) => this.setState({ solutionLoading: false }));
  },

  render: function() {

    let contents;
    if (this.state.initialLoading) {
      contents = <div className="initialLoading">Loading...</div>;
    } else {

      const questions = this.state.questions.map(q => {
        return (
          <li key={q.key}>
            {q.text}
            <img src={this.props.baseUrl + q.key + "/diagram.png"} />
            <button onClick={this.solveQuestion.bind(this, q)}>Solve</button>
            <ChoiceList choices={q.choices} />
          </li>
        );
      });


      let solutionContents;
      if (this.state.displaySolution) {
        if (this.state.solutionLoading) {
          solutionContents = <div className="solutionLoading">Solving...</div>;
        } else {
          solutionContents = (
            <div className="solution">
              <FormulaList className="textParse" title="Text Parse" formulas={this.state.textFormulas} />
              <FormulaList className="diagramParse" title="Diagram Parse" formulas={this.state.diagramFormulas} />
              <FormulaList className="optimized" title="Optimized" formulas={this.state.optimizedFormulas} />
              <Answer answer={this.state.answer} />
            </div>
          )
        }
      }

      contents = (
          <div>
            <ul>{questions}</ul>
            {solutionContents}
          </div>
      );

      /*contents = (
          <div className="demo">
            <h1>Demo</h1>
            <QuestionKeyList updateQuestion={this.updateQuestion} questionKeys={getJSON(this.props.baseUrl+"dirs.json")} />
            <QuestionBox diagramUrl={questionUrl+"diagram.png"} question={question} />
            <ChoiceList choices={question.choices} />
            <FormulaList className="textParse" title="Text Parse" formulas={getJSON(questionUrl+"text_parse.json")} />
            <FormulaList className="diagramParse" title="Diagram Parse" formulas={getJSON(questionUrl+"diagram_parse.json")} />
            <FormulaList className="optimized" title="Optimized" formulas={getJSON(questionUrl+"optimized.json")} />
            <Answer answer={getJSON(questionUrl+"answer.json")} />
          </div>
      )*/
    }
    console.log(contents);

    return (
      <div>
        <header className="padded">Geosolver Demo</header>
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


