const std = @import("std");
const RndGen = std.rand.DefaultPrng;

const stdout = std.io.getStdOut().writer();

const GameBoard = struct {
    allocator: *const std.mem.Allocator,
    size_h: usize,
    size_w: usize,
    board: [][]u8,

    pub fn init(self: *GameBoard, allocator: *const std.mem.Allocator, size_h: usize, size_w: usize) !void {
        self.allocator = allocator;
        self.size_h = size_h;
        self.size_w = size_w;

        self.board = try allocator.alloc([]u8, size_h);
        for (self.board) |*board_row| {
            board_row.* = try allocator.alloc(u8, size_w);
            @memset(board_row.*, @as(u8, 0));
        }
    }

    pub fn print(self: GameBoard) !void {
        try stdout.print("GameBoard({s}", .{""});
        try stdout.print("size_h: {}", .{self.size_h});
        try stdout.print(", size_w: {}", .{self.size_w});
        try stdout.print(", boadr: {{{any}", .{self.board[0]});
        for (self.board[1..self.board.len]) |board_row| {
            try stdout.print(", {any}", .{board_row});
        }
        try stdout.print("}})\n{s}", .{""});
    }

    pub fn free(self: GameBoard) !void {
        for (0..self.board.len) |i| {
            self.allocator.free(self.board[i]);
        }
        self.allocator.free(self.board);
    }
};

pub fn main() !void {
    const size_h: usize = 4;
    const size_w: usize = 6;

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer std.debug.assert(gpa.deinit() == std.heap.Check.ok);
    const allocator = &gpa.allocator();

    var game_board: GameBoard = undefined;
    try game_board.init(allocator, size_h, size_w);
    try game_board.print();

    try game_board.free();
}
