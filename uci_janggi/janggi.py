import subprocess

STOCKFISH_OPTIONS = {
    'Hash':'1024',
    'UCI_Variant':'janggimodern',
}

PIECE_SCORES = {
    'r' : 13,
    'c' : 7,
    'n' : 5,
    'b' : 3,
    'a' : 3,
    'p' : 2,
    'k' : 0,
}

class Janggi:
    def __init__(self, path : str, options = '') -> None:
        self.stock = subprocess.Popen(
            path, universal_newlines = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE
        )

        self.start_engine(options)
        self.table_top_fen = ''
    
    def analyze(self, fen:str, moves:[str], depth:int = 20) -> str:
        'get stock moves and depth to get board and returns info string. This is a generator which yields a analyzing\
            output strings and \'analyze end\' at the end. Make a variable and assign it to this function, and access\
            next anayze by next(<variable name>)'
        self.set_board(fen = fen, stock_moves=moves)

        self.put(f'go depth {depth}')

        while True:
            line = self.read_line().split()
            if len(line) < 0 :
                continue
            elif line[0] == 'bestmove':
                yield 'analyze end'
                break
            elif line[0] == 'info' :
                yield ''.join(line)

    def set_option(self, option:str, value:str) -> None:
        self.put(f'setoption option {option} value {value}')

    def get_best_move(self, depth:int =20) -> None:
        "get the best move."
        self.put(f'go depth {depth}')

        while True:
            line = self.read_line().split()
            if line[0] == 'bestmove':
                return line[1]

    def set_board(self, fen: str, stock_moves: [str]) -> None:
        "get move(stock move list of string) and FEN(string)."
        self.put(f'position fen {fen} moves {" ".join(stock_moves)}')
    
    def get_board_fen(self) -> str:
        'returns FEN string.'
        self.put('d')

        while True:
            line = self.read_line().split()
            if len(line) < 1:
                continue
            elif line[0] == 'Fen:':
                return ' '.join(line[1:])

    def start_engine(self, param) -> None:
        self.put('uci')

        while True:
            line = self.read_line()

            if line == 'uciok':
                break
                
        
        option = STOCKFISH_OPTIONS

        if bool(param):
            option.update(STOCKFISH_OPTIONS)

        for i, j in option.items():
            self.set_option(i, j)
        
        self.put('ucinewgame')
        self.put('position startpos')

        self.put('isready')

        while True:
            line = self.read_line()

            if line == 'readyok':
                break
    
    def read_line(self) -> str:
        'returns text.'
        if not self.stock.stdout:
            raise BrokenPipeError
        else:
            return self.stock.stdout.readline().strip()

    def put(self, text:str) -> None:
        'get text and send it to stockfish.'
        if not self.stock.stdin:
            raise BrokenPipeError
        else:
            self.stock.stdin.write(f'{text}\n')
            self.stock.stdin.flush()