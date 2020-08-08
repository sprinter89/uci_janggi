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

PIECE_NAMES = {
    'r' : '차',
    'c' : '포',
    'n' : '마',
    'b' : '상',
    'a' : '사',
    'p' : '병',
    'P' : '졸',
    'k' : '한',
    'K' : '초'
}

TABLE_TOPS = {
    "상마상마": ["BNA1ABNR", "rbna1abn"],
    "마상마상": ["NBA1ANBR", "rnba1anb"],
    "마상상마": ["NBA1ABNR", "rnba1abn"],
    "상마마상": ["BNA1ANBR", "rbna1anb"] ,
}

class Janggi:
    def __init__(self, path : str, options = '') -> None:
        self.stock = subprocess.Popen(
            path, universal_newlines = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE
        )

        self.start_engine(options)
        self.table_top_fen = ''
    
    def analyze(self, fen:str, moves:[str], depth:int = 20) -> [str]:
        'get stock moves and depth to get board and returns info string'
        self.set_board(fen = fen, stock_moves=moves)

        self.put(f'go depth {depth}')

        lines = []
        while True:
            line = self.read_line().split()
            if len(line) < 0 :
                continue
            elif line[0] == 'bestmove':
                return lines[-1]
            elif line[0] == 'info' :
                lines.append(line)

    def set_option(self, option:str, value:str) -> None:
        self.put(f'setoption option {option} value {value}')

#multi-PV option TODO
    def get_best_move(self, depth:int =20) -> None:
        "get the best move."
        self.put(f'go depth {depth}')

        while True:
            line = self.read_line().split()
            if line[0] == 'bestmove':
                return line[1]

    def set_board(self,*, stock_moves: [str] = '', fen: str='') -> None:
        "get move(stock move list of string) or FEN(string). One of them only expected. Must specify parameter name."
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
