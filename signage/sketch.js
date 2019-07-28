//vars
var playersData = []
var firstPlayer = []
var secondPlayer = []
var thirdPlayer = []
var colfax = {}

let flashState = 0
let firstPlayerImage
let heightOfBox 
let logo
let t = 1

function preload() {
  url = "https://jsonplaceholder.typicode.com/users" ;
  logo = loadImage('logo.png');
  loadJSON(url, dataUpdate, 'jsonp');
  colfax = {
    "regular": loadFont("colfax/Colfax-Regular.otf"),
    "mediumItalic": loadFont("colfax/Colfax-MediumItalic.otf"),
    "black": loadFont("colfax/Colfax-Black.otf"),
    "light": loadFont("colfax/Colfax-Light.otf"),
  }

}
function setup() {
  frameRate(30);
  createCanvas(windowWidth, windowHeight);
  noStroke();
  console.log(TWO_PI);

  rectMode(CORNERS);
  angleMode(DEGREES);

}

function dataUpdate(data) {
    console.log(data)
    playersData = data
    firstPlayer = data[0]
    secondPlayer = data[1]
    thirdPlayer = data[2]
    loadImage('https://pbs.twimg.com/profile_images/604741535775662080/8CEV1nXA.jpg', img => {
      firstPlayerImage = img
    });
}

 
function draw() {

    
    drawLayout()
    drawBottomSection()
    drawTopThree()
    //fill(0)
    //rect(0,0,100,100)
    drawLogo()
    drawLiveDot()
    drawTheRestOfThePlayers()
  // update seconds counter
  if (frameCount % 30 == true) {
    t = t + 1;
  }
  // reload  data
  if (t == 30) {
    // uncomment the line below on production
    //weather = loadJSON(url, dataUpdate, "jsonp");
    console.log("reloaded data");
    t = 0;
  }


}

function drawLayout(){
  rectMode(CORNERS);
    createCanvas(windowWidth, windowHeight);
    background('#f20')
    noStroke()
    rect(29,29,windowWidth-29,windowHeight-29, 20)
    strokeWeight(10);
    stroke('#f20');
    line(windowWidth*0.52, 0, windowWidth*0.52, (windowHeight/5)*4)
    line(0, (windowHeight/5)*4, windowWidth, (windowHeight/5)*4)
    noStroke()
}
function drawBottomSection(){
  rectMode(CORNERS);
  textSize(70);
  fill(0)
  textFont(colfax.mediumItalic);
  textAlign(CENTER, CENTER);
  text("join in: jmss.it/murder",0+29,(windowHeight/5*4)/2, windowWidth-29, windowHeight-29);
}
function drawLogo(){
  let imageFactor = 0.75 // percentage
  image(logo, 29*3-(29/2), 29+29, 512*(imageFactor),192 * (imageFactor));
}
function drawFirstPlace(){
  let widthOfBox = (windowWidth*0.52)-80-50*2
  rectMode(CORNER);

  // set colour & thickness of stroke
  stroke('#f20');
  strokeWeight(4);
  // set fill colour to be white
  fill(255)

  // draw first place box outline
  rect(50,29,widthOfBox,heightOfBox, 20)
  // draw the "1st" text box in red
  fill('#f20')
  // draw the "1st" box so that is is flat against the side
  rect(50,29,(widthOfBox)/3,heightOfBox, 20)
  rect(50+20,29,((widthOfBox)/3)-20,heightOfBox)

  // draw "1st" text
  textSize(60)
  textFont(colfax.black);
  fill(255)
  noStroke()
  textAlign(CENTER, CENTER);
  text("1st",50+20,29,((widthOfBox)/3)-20,heightOfBox);


  // draw first player text
  textSize(28)
  textFont(colfax.regular);
  fill(0)
  noStroke()
  //rect(50 + (((windowWidth/2)-80*3)/3) , 29, (windowWidth/2)-80*3-(((windowWidth/2)-80*3)/3), (windowHeight/8))
  text(firstPlayer.name, 50 + ((widthOfBox)/3) , 29, widthOfBox-((widthOfBox)/3), heightOfBox);
  
  //image(firstPlayerImage ,0,0, heightOfBox*1.2, heightOfBox*1.2, )

}
function drawSecondPlace(){
  let widthOfBox = (windowWidth*0.52)-80-50*2
  rectMode(CORNER);

  // set colour & thickness of stroke
  stroke('#f20');
  strokeWeight(4);
  // set fill colour to be white
  fill(255)

  // draw first place box outline
  rect(50,29,widthOfBox,heightOfBox, 20)
  // draw the "1st" text box in red
  fill('#f20')
  // draw the "1st" box so that is is flat against the side
  rect(50,29,(widthOfBox)/3,heightOfBox, 20)
  rect(50+20,29,((widthOfBox)/3)-20,heightOfBox)

  // draw "1st" text
  textSize(60)
  textFont(colfax.black);
  fill(255)
  noStroke()
  textAlign(CENTER, CENTER);
  text("2nd",50+20,29,((widthOfBox)/3)-20,heightOfBox);


  // draw first player text
  textSize(28)
  textFont(colfax.regular);
  fill(0)
  noStroke()
  //rect(50 + (((windowWidth/2)-80*3)/3) , 29, (windowWidth/2)-80*3-(((windowWidth/2)-80*3)/3), (windowHeight/8))
  text(secondPlayer.name, 50 + ((widthOfBox)/3) , 29, widthOfBox-((widthOfBox)/3), heightOfBox);


}
function drawThirdPlace(){
  let widthOfBox = (windowWidth*0.52)-80-50*2
  rectMode(CORNER);
  // set colour & thickness of stroke
  stroke('#f20');
  strokeWeight(4);
  // set fill colour to be white
  fill(255)

  // draw first place box outline
  rect(50,29,widthOfBox,heightOfBox, 20)
  // draw the "1st" text box in red
  fill('#f20')
  // draw the "1st" box so that is is flat against the side
  rect(50,29,(widthOfBox)/3,heightOfBox, 20)
  rect(50+20,29,((widthOfBox)/3)-20,heightOfBox)

  // draw "1st" text
  textSize(60)
  textFont(colfax.black);
  fill(255)
  noStroke()
  textAlign(CENTER, CENTER);
  text("3rd",50+20,29,((widthOfBox)/3)-20,heightOfBox);


  // draw first player text
  textSize(28)
  textFont(colfax.regular);
  fill(0)
  noStroke()
  //rect(50 + (((windowWidth/2)-80*3)/3) , 29, (windowWidth/2)-80*3-(((windowWidth/2)-80*3)/3), (windowHeight/8))
  text(thirdPlayer.name, 50 + ((widthOfBox)/3) , 29, widthOfBox-((widthOfBox)/3), heightOfBox);
}
function drawTopThree(){
    heightOfBox = (windowHeight/9)
    let paddingTop = 29
    let paddingLeft = 29
    // rotate block
    rotate(-2)
    // migrate block down
    translate(paddingLeft, windowHeight/3-10);
    drawFirstPlace()
    translate(0-5, heightOfBox + paddingTop);
    drawSecondPlace()
    translate(0-5, heightOfBox + paddingTop);
    drawThirdPlace()
    translate(-paddingLeft+5+5, -((windowHeight/3-10)+(heightOfBox+paddingTop)*2))
    rotate(+2)
}
function drawLiveDot(){
  let flashColorArray = [
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#fff",
  "#ffd7d1",
  "#ffc3b9",
  "#ffafa2",
  "#ff9b8b",
  "#ff8674",
  "#ff725d",
  "#ff5e46",
  "#ff4a2e",
  "#ff3617",
  '#ff3617',
  '#ff3617',
  '#ff3617',
  "#ff3617",
  '#ff3617',
  '#ff3617',
  '#ff3617',
  "#ff3617",
  '#ff3617',
  '#ff3617',
  '#ff3617',
  '#ff3617',
  '#ff4a2e',
  '#ff5e46',
  '#ff725d',
  '#ff8674',
  '#ff9b8b',
  '#ffafa2',
  '#ffc3b9',
  '#ffd7d1',
  '#fff' 
]
  
  if (flashState == flashColorArray.length-1){
    flashState = 0
  } else {
      flashState = flashState + 1
  }

  translate(10,10)
  fill(flashColorArray[flashState])
  ellipse(windowWidth*0.52+15, 39, 20)
  textFont(colfax.regular)
  fill("#f20")
  text("LIVE", windowWidth*0.52+35+25 , 39)
  translate(-10,-10)
}
function drawTheRestOfThePlayers() {
  rectMode(CORNERS)
  fill(0)
  
  
  textFont(colfax.light)
  textSize(20)
  var i;
  for (i = 3; i < playersData.length; i++) { 
    let padding = (33)*(i-3)
    let _text 
    if (playersData[i].isDead != true){
      fill(0)
    switch (i) {
      case 0 | 1 | 2:
        // do nothing
        break;
      case 21:
          _text= i+"st - "+playersData[i].name
        break;
      case 22:
          _text= i+"nd - "+playersData[i].name
        break;
      case 23:
          _text= i+"rd - "+playersData[i].name
        break;
      default:
          //rect(windowWidth*0.52 , 29*2+padding, (windowWidth-29)/2, (windowHeight/5)*4)
         _text= i+"th - "+playersData[i].name
        break;
      
    }
    
  } else{
    // show dead
    fill ("#f20")
  }
  if (29*2+padding >= windowHeight/5*4){
    textAlign(LEFT, TOP)
    padding = (33)*(i-20)
    text(_text, (windowWidth*(1-0.52))+(windowWidth*0.52/2) , (29*2+(padding))-20, (windowWidth-29), (windowHeight/5)*4)
  } else{
    textAlign(LEFT, TOP)
    text(_text, windowWidth*0.52+29 , (29*2+padding)-15, (windowWidth-29)/4, (windowHeight/5)*4)
  }
  }
 
}