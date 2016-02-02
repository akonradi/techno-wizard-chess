#!/usr/bin/env python

import rospy
from wizard_chess.msg import *
from wizard_chess.srv import ScanBoard, ScanBoardResponse

board_pieces = [] # initialized in dummy_board_main

def handle_scan_board(req):
  return ScanBoardResponse(board_pieces)

def handle_move_piece(msg):
  global board_pieces

  # Don't worry about the rules here - that's some other node's job
  moving = (filter(lambda p: p.pos == msg.start, board_pieces) or [None])[0]

  if moving is not None:
    # Remove any piece at the destination
    board_pieces = filter(lambda p: p.pos != msg.end, board_pieces)
    moving.pos = msg.end
  

def dummy_board_main():
  global board_pieces

  white_start = [
    (ChessPiece.ROOK,   (0, 0)),
    (ChessPiece.KNIGHT, (1, 0)),
    (ChessPiece.BISHOP, (2, 0)),
    (ChessPiece.QUEEN,  (3, 0)),
    (ChessPiece.KING,   (4, 0)),
    (ChessPiece.BISHOP, (5, 0)),
    (ChessPiece.KNIGHT, (6, 0)),
    (ChessPiece.ROOK,   (7, 0)),
  ] + [
    (ChessPiece.PAWN, (x, 1)) for x in range(8)
  ]

  start_state = [(ChessPiece.WHITE, p) for p in white_start] + \
    [(ChessPiece.BLACK, (t, (x, 7 - y)))
      for (t, (x, y)) in white_start]

  board_pieces = [
    PositionedPiece(piece=ChessPiece(type=t, color=player),
                    pos=BoardPosition(x=x, y=y))
    for (player, (t, (x, y))) in start_state]

  rospy.init_node('board_server')
  s = rospy.Service('scan_board', ScanBoard, handle_scan_board)
  m = rospy.Subscriber('moved_piece', MovePiece, handle_move_piece)
  rospy.spin()

if __name__ == "__main__":
  dummy_board_main()
