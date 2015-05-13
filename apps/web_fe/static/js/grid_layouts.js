function returnBalanced(canvasSizeX, canvasSizeY){

	return [
[{ //1 grid
	row:function(canvasSizeY){
		return 1;
	},
	col:function(canvasSizeY){
		return 1;
	},
	sizex:function(canvasSizeY){
		return canvasSizeX;
	},
	sizey:function(canvasSizeY){
		return canvasSizeY;
	},
}],
[{ //2 grids
	row:function(canvasSizeY){
		return 1;
	},
	col:function(canvasSizeY){
		return 1;
	},
	sizex:function(canvasSizeX){
		if(canvasSizeX%2 != 0){
			return Math.floor(canvasSizeX/2);
		} else {
			return canvasSizeX/2;
		}
	},
	sizey:function(canvasSizeY){
		return canvasSizeY;
	},
},{
	row:function(canvasSizeY){
		return 1;
	},
	col:function(canvasSizeX){
		if(canvasSizeX%2 != 0){
			return Math.floor(canvasSizeX/2)+1;
		} else {
			return canvasSizeX/2+1;
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
		return canvasSizeY;
	},
}],
[{ //3 grids
	row:function(canvasSizeY){
		return 1;
}, //top
col:function(canvasSizeY){
	return 1;
},
sizex:function(canvasSizeY){
	return canvasSizeX;
},
sizey:function(canvasSizeY){
	if(canvasSizeY%2 != 0){
		return Math.floor(canvasSizeY/2);
	} else {
		return canvasSizeY/2;
	}
}},{
row:function(canvasSizeY){ //bottom left
	if(canvasSizeY%2 != 0){
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeY){
	return 1;
},
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
}},{
row:function(canvasSizeY){ //bottom right
	if(canvasSizeY%2 != 0){
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%2 != 0){
		return Math.floor(canvasSizeX/2)+1;
	} else {
		return canvasSizeX/2+1;
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
}}],
[{ //4 grids
	row:function(canvasSizeY){
		return 1;
}, //top left
col:function(canvasSizeY){
	return 1;
},
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
	row:function(canvasSizeY){
		return 1;
}, //top right
col:function(canvasSizeX){
	if(canvasSizeX%2 != 0){
		return Math.floor(canvasSizeX/2)+1;
	} else {
		return canvasSizeX/2+1;
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
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeY){
	return 1;
},
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
row:function(canvasSizeY){ // bottom right
	if(canvasSizeY%2 != 0){
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%2 != 0){
		return Math.floor(canvasSizeX/2)+1;
	} else {
		return canvasSizeX/2+1;
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
	row:function(canvasSizeY){
		return 1;
}, //top left
col:function(canvasSizeY){
	return 1;
},
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
	row:function(canvasSizeY){
		return 1;
}, //top right
col:function(canvasSizeX){ 
	if(canvasSizeX%2 != 0){
		return Math.floor(canvasSizeX/2)+1;
	} else {
		return canvasSizeX/2+1;
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
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeY){
	return 1;
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
row:function(canvasSizeY){ //bottom middle
	if(canvasSizeY%2 != 0){
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){ 
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)+1;
	} else {
		return canvasSizeX/3+1;
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
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){ 
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)*2+1;
	} else {
		return 2*canvasSizeX/3+1;
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
	row:function(canvasSizeY){
		return 1;
}, //top left
col:function(canvasSizeY){
	return 1;
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
		return Math.floor(canvasSizeY/2);
	} else {
		return canvasSizeY/2;
	}
}
},{
	row:function(canvasSizeY){
		return 1;
}, // top middle
col:function(canvasSizeX){ 
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)+1;
	} else {
		return canvasSizeX/3+1;
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
		return Math.floor(canvasSizeY/2);
	} else {
		return canvasSizeY/2;
	}
}
},{
	row:function(canvasSizeY){
		return 1;
}, //top right
col:function(canvasSizeX){ 
	if(canvasSizeX%3 != 0){
		return Math.floor(2*canvasSizeX/3)+1;
	} else {
		return 2*canvasSizeX/3+1;
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
		return Math.floor(canvasSizeY/2);
	} else {
		return canvasSizeY/2;
	}
}
},{
row:function(canvasSizeY){ //bottom left
	if(canvasSizeY%2 != 0){
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeY){
	return 1;
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
row:function(canvasSizeY){ //bottom middle
	if(canvasSizeY%2 != 0){
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){ 
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)+1;
	} else {
		return canvasSizeX/3+1;
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
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){ 
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)*2+1;
	} else {
		return 2*canvasSizeX/3+1;
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
[{ //7 grids
	row:function(canvasSizeX){
		return 1;
}, //top left
col:function(canvasSizeX){
	return 1;
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
	row:function(canvasSizeX){
		return 1;
}, // top middle left
col:function(canvasSizeX){ 
	if(canvasSizeX%4 != 0){
		return Math.floor(canvasSizeX/4)+1;
	} else {
		return canvasSizeX/4+1;
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
	row:function(canvasSizeX){
		return 1;
}, // top middle right
col:function(canvasSizeX){ 
	if(canvasSizeX%4 != 0){
		return Math.floor(canvasSizeX/4)*2+1;
	} else {
		return 2*canvasSizeX/4+1;
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
	row:function(canvasSizeX){
		return 1;
}, //top right
col:function(canvasSizeX){ 
	if(canvasSizeX%4 != 0){
		return Math.floor(canvasSizeX/4)*3+1;
	} else {
		return 3*canvasSizeX/4+1;
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
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){
	return 1;
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
row:function(canvasSizeY){//bottom middle
	if(canvasSizeY%2 != 0){
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){//bottom middle
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)+1;
	} else {
		return canvasSizeX/3+1;
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
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)*2+1;
	} else {
		return 2*canvasSizeX/3+1;
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
	row:function(canvasSizeX){
		return 1
}, //top left
col:function(canvasSizeX){
	return 1
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
	row:function(canvasSizeX){
		return 1
}, //top middle left
col:function(canvasSizeX){//bottom middle
	if(canvasSizeX%4 != 0){
		return Math.floor(canvasSizeX/4)+1;
	} else {
		return canvasSizeX/4+1;
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
	row:function(canvasSizeX){
		return 1
}, //top middle right
col:function(canvasSizeX){
	if(canvasSizeX%4 != 0){
		return Math.floor(canvasSizeX/4)*2+1;
	} else {
		return 2*canvasSizeX/4+1;
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
	row:function(canvasSizeX){
		return 1
}, // top right
col:function(canvasSizeY){
	if(canvasSizeY%4 != 0){
		return Math.floor(canvasSizeY/4)*3+1;
	} else {
		return 3*canvasSizeY/4+1;
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
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){
	return 1
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
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%4 != 0){
		return Math.floor(canvasSizeX/4)+1;
	} else {
		return canvasSizeX/4+1;
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
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%4 != 0){
		return Math.floor(canvasSizeX/4)*2+1;
	} else {
		return 2*canvasSizeX/4+1;
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
row:function(canvasSizeY){ //bottom right
	if(canvasSizeY%2 != 0){
		return Math.floor(canvasSizeY/2)+1;
	} else {
		return canvasSizeY/2+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%4 != 0){
		return Math.floor(canvasSizeX/4)*3+1;
	} else {
		return 3*canvasSizeX/4+1;
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
row:function(canvasSizeY){ //top left
	return 1
}, 
col:function(canvasSizeX){
	return 1
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
row:function(canvasSizeY){ //top middle
	return 1
}, 
col:function(canvasSizeX){
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)+1
	} else {
		return canvasSizeX/3+1;
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
row:function(canvasSizeY){ //top right
	return 1
}, 
col:function(canvasSizeX){
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)*2+1;
	} else {
		return 2*canvasSizeX/3+1;
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
		return Math.floor(canvasSizeY/3)+1;
	} else {
		return canvasSizeY/3+1;
	}
},
col:function(canvasSizeX){
	return 1
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
row:function(canvasSizeY){ // middle middle
	if(canvasSizeY%3 != 0){
		return Math.floor(canvasSizeY/3)+1;
	} else {
		return canvasSizeY/3+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)+1;
	} else {
		return canvasSizeX/3+1;
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
		return Math.floor(canvasSizeY/3)+1;
	} else {
		return canvasSizeY/3+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)*2+1;
	} else {
		return 2*canvasSizeX/3+1;
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
		return Math.floor(canvasSizeY/3)*2+1;
	} else {
		return 2*canvasSizeY/3+1;
	}
},
col:function(canvasSizeX){
	return 1
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
row:function(canvasSizeY){ // bottom middle
	if(canvasSizeY%3 != 0){
		return Math.floor(canvasSizeY/3)*2+1;
	} else {
		return 2*canvasSizeY/3+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)+1;
	} else {
		return canvasSizeX/3+1;
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
		return Math.floor(canvasSizeY/3)*2+1;
	} else {
		return 2*canvasSizeY/3+1;
	}
},
col:function(canvasSizeX){
	if(canvasSizeX%3 != 0){
		return Math.floor(canvasSizeX/3)*2+1;
	} else {
		return 2*canvasSizeX/3+1;
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
}]];
}
