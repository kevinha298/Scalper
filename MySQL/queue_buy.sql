CREATE TABLE queue_buy (
	symbol varchar(10),
	buy_qty int,
	buy_price decimal(18,2),
	max_position_qty int,
	max_buy_price decimal(18,2),
	min_buy_price decimal(18,2),
    buy_sell_cents_buffer INT
)


