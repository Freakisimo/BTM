var labelType, useGradients, nativeTextSupport, animate;
      (function() {
        var ua = navigator.userAgent,
            iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
            typeOfCanvas = typeof HTMLCanvasElement,
            nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
            textSupport = nativeCanvasSupport 
              && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
        //I'm setting this based on the fact that ExCanvas provides text support for IE
        //and that as of today iPhone/iPad current text support is lame
        labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
        nativeTextSupport = labelType == 'Native';
        useGradients = nativeCanvasSupport;
        animate = !(iStuff || !nativeCanvasSupport);
      })();

      var Log = {
        elem: false,
        write: function(text){
          if (!this.elem) 
            this.elem = document.getElementById('log');
          this.elem.innerHTML = text;
          this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
        }
      };


      function init(datos){
        //init data
        var json = datos;
        //end
        //init TreeMap
        var tm = new $jit.TM.Squarified({
          //where to inject the visualization
          injectInto: 'infovis',
          //parent box title heights
          titleHeight: 20,
          //enable animations
          animate: animate,
          //box offsets
          offset: 1,
          //Attach left and right click events
          Events: {
            enable: true,
            onClick: function(node) {
              if(node) tm.enter(node);
              var nom = node.name.substring(0,2);
              if(nom == 'H ' || nom == 'M ') Grafico(node);
              $('#nivel').val(node.id);
            },
            onRightClick: function() {
              tm.out();
              //$('#nivel').val(node.parent.id);
              overlayHide();
            }
          },
          duration: 1000,
          //Enable tips
          Tips: {
            enable: false,
            //add positioning offsets
            offsetX: 20,
            offsetY: 20,
            //implement the onShow method to
            //add content to the tooltip when a node
            //is hovered
            
          },
          //Add the name of the node in the correponding label
          //This method is called once, on label creation.
          onCreateLabel: function(domElement, node){
              domElement.innerHTML = node.name;
              var style = domElement.style;
              style.display = '';
              style.border = '1px solid transparent';
              domElement.onmouseover = function() {
                style.border = '1px solid #9FD4FF';
              };
              domElement.onmouseout = function() {
                style.border = '1px solid transparent';
              };
          }
        });
        tm.loadJSON(json);
        tm.refresh();
        //end
        //add events to radio buttons
        var sq = $jit.id('r-sq'),
            st = $jit.id('r-st'),
            sd = $jit.id('r-sd');
        var util = $jit.util;
        util.addEvent(sq, 'change', function() {
          if(!sq.checked) return;
          util.extend(tm, new $jit.Layouts.TM.Squarified);
          tm.refresh();
        });
        util.addEvent(st, 'change', function() {
          if(!st.checked) return;
          util.extend(tm, new $jit.Layouts.TM.Strip);
          tm.layout.orientation = "v";
          tm.refresh();
        });
        util.addEvent(sd, 'change', function() {
          if(!sd.checked) return;
          util.extend(tm, new $jit.Layouts.TM.SliceAndDice);
          tm.layout.orientation = "v";
          tm.refresh();
        });
        //add event to the back button
        var back = $jit.id('back');
        $jit.util.addEvent(back, 'click', function() {
          tm.out();
        });
      }



function Grafico(nodo) {
  //alert(nodo.data.playcount);
  var lido = nodo.data.lido * 100
  lido = lido.toFixed(2)

  var bupre = nodo.data.bupre * 100
  bupre = bupre.toFixed(2)

  bupre = parseFloat(bupre);
  lido = parseFloat(lido);

  var chart = $('#overlay').highcharts();
  chart.series[0].data[0].update(lido);
  chart.series[1].data[0].update(bupre);
  //chart.yAxis[0].setExtremes(0,1600);

  overlay();
}
function overlay() {
  el = document.getElementById("overlay");
  el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function overlayHide() {
  el = document.getElementById("overlay");
  el.style.visibility = "hidden";
}