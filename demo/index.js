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
              {this.props.key}: {this.props.value}
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
                    <Choice key={key} value={this.props.choices[key]} />
                );
            }
        }
        return (
            <div className="choiceList">
                <h2>Choices</h2>
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
        var formulaNodes = this.props.formulas.map(function (formula) {
            return (
                <Formula formula={formula}/>
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

function getJSON(url) {
    var out;
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        success: function(data) {out = data},
        async: false
    });
    return out;
}

var Demo = React.createClass({
    getInitialState: function() {
        return {questionKey: this.props.defaultQuestionKey}
    },
    updateQuestion: function(questionKey) {
        console.log(questionKey);
        this.setState({questionKey: questionKey});
    },
    render: function() {
        var questionUrl = this.props.baseUrl + this.state.questionKey + "/";
        var question = getJSON(questionUrl+"question.json");
        return (
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
        );
    }
});

React.render(
    <Demo baseUrl="assets/" defaultQuestionKey="968" />,
    document.getElementById('content')
);

