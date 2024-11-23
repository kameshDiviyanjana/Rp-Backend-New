export class customError extends Error{
    constructor(massage, statuscode){
        super(massage);
        this.statuscode = statuscode;
        this.status = statuscode >= 400 && statuscode < 500 ? 'fail' : 'error';
        this.isOpreationl =true;

        Error.captureStackTrace(this,this.constructor)
    }



}

//next is must  and goable error hanble is must

