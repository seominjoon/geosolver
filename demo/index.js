var Question = React.createClass({
    render: function() {
        return (
            <div className="question">
                <h3>Question</h3>
            </div>
        );
    }
});

var QuestionList = React.createClass({
    render: function() {
        return (
            <div className="questionList">
                <h2>Question List</h2>
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
                {this.props.formula.formula}: {this.props.formula.score}
            </div>
        );
    }
});

var FormulaList = React.createClass({
    render: function() {
        console.log(this.props.formulas);
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
    handleChooseQuestion: function(questionKey) {
    },
    render: function() {
        var questionUrl = this.props.baseUrl + this.state.questionKey + "/";
        return (
            <div className="demo">
                <h1>Demo</h1>
                <QuestionList onChooseQuestion={this.handleChooseQuestion} dirs={getJSON(this.props.baseUrl+"dirs.json")} />
                <QuestionBox diagramUrl={questionUrl+"diagram.png"} question={getJSON(questionUrl+"question.json")} />
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

