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
                <h2>Question Box</h2>
            </div>
        );
    }
});

var Formula = React.createClass({
    render: function() {
        return (
            <div className="formula">
                <h3>Formula</h3>
            </div>
        );
    }
});

var FormulaList = React.createClass({
    render: function() {
        return (
            <div className={this.props.className}>
                <h2>{this.props.title}</h2>
            </div>
        );
    }
});


var Answer = React.createClass({
    render: function() {
        return (
            <div className="answer">
                <h2>Answer</h2>
            </div>
        );
    }
});

var Demo = React.createClass({
    getInitialState: function() {
      return {questionKey: this.props.default};
    },
    handleChooseQuestion: function(questionKey) {
    },
    render: function() {
        return (
            <div className="demo">
                <h1>Demo</h1>
                <QuestionList onChooseQuestion={this.handleChooseQuestion} dirs={$.getJSON(this.props.baseUrl+"dirs.json")}/>
                <QuestionBox
                <FormulaList className="textParse" title="Text Parse" formulas={$.getJSON(this.props.baseUrl+this.state.questionKey+"/text_parse.json")} />
                <FormulaList className="diagramParse" title="Diagram Parse" formulas={$.getJSON(this.props.baseUrl+this.state.questionKey+"/diagram_parse.json")} />
                <FormulaList className="optimized" title="Optimized" formulas={$.getJSON(this.props.baseUrl+this.state.questionKey+"/optimized.json")} />
                <Answer answer={$.getJSON(this.props.baseUrl+this.state.questionKey+"/answer.json")} />
            </div>
        );
    }
});

React.render(
    <Demo baseUrl="assets/" default="968" />,
    document.getElementById('content')
);

/*
 var rootPath = "assets/";
 var dirsJsonPath = rootPath + "dirs.json";
 var basePath = rootPath + "968/";
 var questionJsonPath = basePath + "question.json";
 var textParseJsonPath = basePath + "text_parse.json";
 var diagramParseJsonPath = basePath + "diagram_parse.json";
 var optimizedJsonPath = basePath + "optimized.json";
 var answerJsonPath = basePath + "answer.json";
 $.getJSON( questionJsonPath, function( data ) {
 var text = data.text;
 var diagramPath = basePath + data.diagram_path;
 $('#text').text(text);
 $('#diagram').attr("src", diagramPath);
 });

 function loadFormulas(jsonPath, id) {
 $.getJSON( jsonPath, function( data ) {
 var textParseItems = [];
 for (var i = 0; i < data.length; i++) {
 textParseItems.push("<li>" + data[i].formula + "</li>");
 }
 $("#" + id).html(textParseItems.join(""));
 });
 }

 loadFormulas(textParseJsonPath, "textParse");
 loadFormulas(diagramParseJsonPath, "diagramParse");
 loadFormulas(optimizedJsonPath, "optimized");

 $.getJSON( answerJsonPath, function( data ) {
 $('#answer').text(data.answer);
 });
 */

