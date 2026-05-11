use nbcl::NbclEngine;
use rhai::Engine;
use koto::Koto;
use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    let parse_only = args.contains(&"--parse-only".to_string());
    
    if args.len() < 4 {
        eprintln!("Usage: nbcl-benchmarks --lang <nbcl|rhai|koto> <file> [--parse-only]");
        std::process::exit(1);
    }

    let lang = args.iter().position(|a| a == "--lang")
        .and_then(|i| args.get(i + 1))
        .expect("Missing --lang argument");
        
    let path = args.last().expect("Missing file path");

    let source = fs::read_to_string(path).unwrap_or_else(|e| {
        eprintln!("Could not read {path}: {e}");
        std::process::exit(1);
    });

    match lang.as_str() {
        "nbcl" => run_nbcl(&source, parse_only),
        "rhai" => run_rhai(&source, parse_only),
        "koto" => run_koto(&source, parse_only),
        _ => eprintln!("Unknown language: {lang}"),
    }
}

fn run_nbcl(source: &str, parse_only: bool) {
    let engine = NbclEngine::new();
    match engine.parse_str(source) {
        Ok(ast) => {
            if parse_only { return; }
            match engine.evaluate(ast) {
                Ok(evaled) => println!("{:#?}", evaled),
                Err(e) => println!("{}", e),
            }
        }
        Err(e) => eprintln!("{}", e),
    }
}

fn run_rhai(source: &str, parse_only: bool) {
    let engine = Engine::new();
    match engine.compile(source) {
        Ok(ast) => {
            if parse_only { return; }
            match engine.eval_ast::<rhai::Dynamic>(&ast) {
                Ok(result) => println!("{}", result),
                Err(e) => eprintln!("Rhai Runtime Error: {}", e),
            }
        }
        Err(e) => eprintln!("Rhai Parse Error: {}", e),
    }
}

fn run_koto(source: &str, parse_only: bool) {
    let mut koto = Koto::default();
    match koto.compile(source) {
        Ok(chunk) => {
            if parse_only { return; }
            match koto.run(chunk) {
                Ok(result) => println!("{:#?}", result),
                Err(e) => eprintln!("Koto Runtime Error: {}", e),
            }
        }
        Err(e) => eprintln!("Koto Compile Error: {}", e),
    }
}