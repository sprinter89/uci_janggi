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
    
    # def set_table_top(self, cho:str, han:str) -> None:
    #     fen = TABLE_TOPS[han][1] + "r/4k4/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/4K4/R" + TABLE_TOPS[cho][0] + " w - - 0 1"
    #     self.set_board(fen=fen)
    #     self.table_top_fen = fen

    # def trans_coord(self,*, kor_coord:str='', stock_coord:str='', fen:str='') -> None:
    #     if bool(kor_coord) and bool(stock_coord):
    #         print('error')
    #     elif bool(kor_coord):
    #         translated = ''
    #         for char in kor_coord:
    #             if char.isdecimal():
    #                 translated += char
    #         kor_coord = translated[0:2][::-1] + translated[2:4][::-1]

    #         translated = ['', '', '', '']

    #         for i in range(2):
    #             translated[i*2] = chr(ord(kor_coord[i*2])+48)
                
    #             if kor_coord[i*2+1] == '0':
    #                 translated[i*2+1] = '1'
    #             elif kor_coord[i*2+1] == '1':
    #                 translated[i*2+1] = '10'
    #             else:
    #                 translated[i*2+1] = str(10 - int(kor_coord[i*2+1])+ 1)
    #         translated = ''.join(translated)
    #         return translated
    #     elif bool(stock_coord):
    #         translated = []
            
    #         carry = 0
    #         for i in range(4):
    #             if stock_coord[i + carry].isdecimal():
    #                 if stock_coord[i:i+2] == '10':
    #                     carry = 1
    #                     translated.append('10')
    #                     continue
    #             translated.append(stock_coord[i+carry])
            
    #         translated = translated[0:2][::-1] + translated[2:4][::-1]

    #         stock_coord = ['', '', '', '']

    #         for i in range(2):
    #             if translated[i*2] == '10':
    #                 stock_coord[i*2] = '1'
    #             elif translated[i*2] == '0':
    #                 stock_coord[i*2] = '0'
    #             else:
    #                 stock_coord[i*2] = str(10 - int(translated[i*2]) + 1)
                
    #             stock_coord[i*2+1] = chr(ord(translated[i*2+1])-48)
    #         stock_coord.insert(2,self.get_piece_kor(stock_coord[0:2]))
            
    #         return ''.join(stock_coord)
            
    # def get_piece_kor(self, coord:str, fen:str='') -> str:
    #     orig_board = self.get_board_fen()
    #     if bool(fen):
    #         self.set_board(fen = fen)
    #     else:
    #         fen = orig_board
    #     divided_fen = fen.split()[0].split('/')
        
    #     board = []
    #     for rank in divided_fen:
    #         board_line = ''
    #         for square in rank:
    #             if square.isdecimal():
    #                 for _ in range(int(square)):
    #                     board_line += ' '
    #             else:
    #                 board_line += square
    #         board.append(board_line)
        
    #     if coord[0] == '0':
    #         piece = board[9][int(coord[1])-1]
    #     else:
    #         piece = board[int(coord[0])-1][int(coord[1])-1]

    #     if piece == ' ':
    #         return ' '
    #     elif piece.lower() == 'p' or piece.lower() == 'k':
    #         piece = PIECE_NAMES[piece]
    #     else:
    #         piece = PIECE_NAMES[piece.lower()]
        
    #     self.set_board(fen=orig_board)

    #     return piece

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

    # def is_move_legal(self, move:str) -> bool:
    #     "check if the move is legal on current board. returns bool."
    #     self.put(f'go depth 1 searchmoves {move}')

    #     while True:
    #         line = self.read_line().split()
    #         if line[0] == 'bestmove':
    #             if  line[1] == move:
    #                 return True
    #             else:
    #                 return False

    def set_board(self,*, stock_moves: [str] = '', fen: str='') -> None:
        "get move(stock move list of string) or FEN(string). One of them only expected. Must specify parameter name."
        self.put(f'position fen {fen} moves {" ".join(stock_moves)}')
#TODO make image
    # def image_board(self, kor_coord:str = '') -> None:
    # 	pass
    
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
