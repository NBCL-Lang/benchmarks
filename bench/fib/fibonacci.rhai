fn fibonacci(n) {
    let a = 0;
    let b = 1;
    
    for i in 0..n { 
        print(a);
        
        let temp = a;
        a = b;
        b = temp + b;
    }
}

fibonacci(5000);