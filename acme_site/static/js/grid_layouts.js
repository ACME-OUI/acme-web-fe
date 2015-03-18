
/**
 * returns the layout specifications for a balanced layout
 * canvasSizeX, canvasSizeY are the size of the grid canvas
 * --> Im only doing this for 9 grids right now until I get the names for the next 3
 */
function returnBalanced(canvasSizeX, canvasSizeY){

	return [
		[{ //1 grid
			row:1,
			col:1,
			sizex:canvasSizeX,
			sizey:canvasSizeY,
		}],
		[{ //2 grids
			row:1,
			col:1,
			sizex:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:canvasSizeY
		},{
			row:1,
			col:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			sizex:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2)+1;
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:canvasSizeY
		}],
		[{ //3 grids
			row:1, //top
			col:1,
			sizex:canvasSizeX,
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeX){ //bottom left
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			col:1,
			sizex:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeX){ //bottom right
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			col:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			sizex:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2)+1;
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		}],
		[{ //4 grids
			row:1, //top left
			col:1,
			sizex:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:1, //top right
			col:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			sizex:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2)+1;
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeX){ //bottom left
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			col:1
			sizex:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeX){ // bottom right
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			col:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			sizex:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2)+1;
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		}],
		[{ //5 grids
			row:1, //top left
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:1, //top right
			col:function(canvasSizeX){ 
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			sizex:function(canvasSizeX){
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2)+1;
				} else {
					return canvasSizeX/2;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeY){ //bottom left
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeY){ //bottom middle
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(2*canvasSizeX/3);
				} else {
					return 2*canvasSizeX/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeY){ //bottom right
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(2*canvasSizeX/3);
				} else {
					return 2*anvasSizeX/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3)+canvasSizeX%3;
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		}],
		[{ //6 grids
			row:1, //top left
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:1, // top middle
			col:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(2*canvasSizeX/3);
				} else {
					return 2*canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:1, //top right
			col:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(2*canvasSizeX/3);
				} else {
					return 2*canvasSizeX/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(2*canvasSizeX/3)+canvasSizeX%3;
				} else {
					return 2*canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeX){ //bottom left
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(2*canvasSizeX/3);
				} else {
					return 2*canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeX){ //bottom middle
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			col:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(2*canvasSizeX/3);
				} else {
					return 2*canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeX){ //bottom right
				if(canvasSizeX%2 != 0){
					return Math.floor(canvasSizeX/2);
				} else {
					return canvasSizeX/2;
				}
			},
			col:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(2*canvasSizeX/3);
				} else {
					return 2*canvasSizeX/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(2*canvasSizeX/3)+canvasSizeX%3;
				} else {
					return 2*canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		}],
		[{ //7 grids
			row:1, //top left
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4);
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:1, // top middle left
			col:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(2*canvasSizeX/4);
				} else {
					return 2*canvasSizeX/4;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4);
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},
		{
			row:1, // top middle right
			col:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(2*canvasSizeX/4);
				} else {
					return 2*canvasSizeX/4;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4);
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},
		{
			row:1, //top right
			col:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(3*canvasSizeX/4);
				} else {
					return 3*canvasSizeX/4;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4)+canvasSizeX%4;
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},
		{
			row:function(canvasSizeY){//bottom left
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},
		{
			row:function(canvasSizeY){//bottom middle
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:function(canvasSizeY){//bottom middle
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},
		{
			row:function(canvasSizeY){//bottom right
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:function(canvasSizeY){//bottom middle
				if(canvasSizeY%3 != 0){
					return Math.floor(2*canvasSizeY/3);
				} else {
					return 2*canvasSizeY/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3)+canvasSizeX%3;
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		}],
		[{ //8 grids
			row:1, //top left
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4);
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:1, //top middle left
			col:function(canvasSizeY){//bottom middle
				if(canvasSizeY%4 != 0){
					return Math.floor(canvasSizeY/4);
				} else {
					return canvasSizeY/4;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4);
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:1, //top middle right
			col:function(canvasSizeY){
				if(canvasSizeY%4 != 0){
					return Math.floor(2*canvasSizeY/4);
				} else {
					return 2*canvasSizeY/4;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4);
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:1, // top right
			col:function(canvasSizeY){
				if(canvasSizeY%4 != 0){
					return Math.floor(3*canvasSizeY/4);
				} else {
					return 3*canvasSizeY/4;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4)+canvasSizeX%4;
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeY){ //bottom left
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4);
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeY){ //bottom middle left
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:function(canvasSizeY){
				if(canvasSizeY%4 != 0){
					return Math.floor(2*canvasSizeY/4);
				} else {
					return 2*canvasSizeY/4;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4);
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeY){ //bottom middle right
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:function(canvasSizeY){
				if(canvasSizeY%4 != 0){
					return Math.floor(2*canvasSizeY/4);
				} else {
					return 2*canvasSizeY/4;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4);
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		},{
			row:function(canvasSizeY){ //bottom middle left
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2);
				} else {
					return canvasSizeY/2;
				}
			},
			col:function(canvasSizeY){
				if(canvasSizeY%4 != 0){
					return Math.floor(3*canvasSizeY/4);
				} else {
					return 3*canvasSizeY/4;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%4 != 0){
					return Math.floor(canvasSizeX/4)+canvasSizeX%4;
				} else {
					return canvasSizeX/4;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%2 != 0){
					return Math.floor(canvasSizeY/2)+1;
				} else {
					return canvasSizeY/2;
				}
			}
		}],
		[{ //9 grids
			row:1, //top left
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			}
		},{
			row:1, //top middle
			col:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			}
		},{
			row:1, //top right
			col:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(2*canvasSizeY/3);
				} else {
					return 2*canvasSizeY/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3)+canvasSizeX%3;
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			}
		},{
			row:function(canvasSizeY){ // middle left
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			}
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3)+canvasSizeX%3;
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			}
		},{
			row:function(canvasSizeY){ // middle middle
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			}
			col:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(2*canvasSizeY/3);
				} else {
					return 2*canvasSizeY/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			}
		},{
			row:function(canvasSizeY){ // middle right
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			},
			col:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(2*canvasSizeY/3);
				} else {
					return 2*canvasSizeY/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3)+canvasSizeX%3;
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			}
		},{
			row:function(canvasSizeY){ // bottom left
				if(canvasSizeY%3 != 0){
					return Math.floor(2*canvasSizeY/3);
				} else {
					return 2*canvasSizeY/3;
				}
			}
			col:1,
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3)+canvasSizeX%3;
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3)+canvasSizeY%3;
				} else {
					return canvasSizeY/3;
				}
			}
		},{
			row:function(canvasSizeY){ // bottom middle
				if(canvasSizeY%3 != 0){
					return Math.floor(2*canvasSizeY/3);
				} else {
					return 2*canvasSizeY/3;
				}
			}
			col:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3);
				} else {
					return canvasSizeY/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3);
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3)+canvasSizeY%3;
				} else {
					return canvasSizeY/3;
				}
			}
		},{
			row:function(canvasSizeY){ // bottom right
				if(canvasSizeY%3 != 0){
					return Math.floor(2*canvasSizeY/3);
				} else {
					return 2*canvasSizeY/3;
				}
			},
			col:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(2*canvasSizeY/3);
				} else {
					return 2*canvasSizeY/3;
				}
			},
			sizex:function(canvasSizeX){ 
				if(canvasSizeX%3 != 0){
					return Math.floor(canvasSizeX/3)+canvasSizeX%3;
				} else {
					return canvasSizeX/3;
				}
			},
			sizey:function(canvasSizeY){
				if(canvasSizeY%3 != 0){
					return Math.floor(canvasSizeY/3)+canvasSizeY%3;
				} else {
					return canvasSizeY/3;
				}
			}
		}]
	];
}