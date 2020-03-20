USE 'DFxpZwam46';
DROP procedure IF EXISTS 'add_new_filled_order';

DELIMITER $$
USE 'DFxpZwam46'$$
CREATE DEFINER='add_new_filled_order'@'remotemysql.com' PROCEDURE 'add_new_filled_order'()
BEGIN
	INSERT INTO filled_order (asset_class, asset_id, canceled_at, client_order_id, created_at, expired_at, failed_at, filled_at, filled_avg_price,
             filled_qty, id, limit_price, order_type, qty, side,  status, stop_price, submitted_at, symbol, time_in_force, type, updated_at)
	SELECT asset_class, asset_id, canceled_at, client_order_id, created_at, expired_at, failed_at, filled_at, filled_avg_price,
             filled_qty, id, limit_price, order_type, qty, side,  status, stop_price, submitted_at, symbol, time_in_force, type, updated_at
	FROM filled_order_stage
    WHERE id NOT IN (SELECT id FROM filled_order);

    CALL add_transaction_buy;
    CALL add_transaction_sell;

END$$

DELIMITER ;
