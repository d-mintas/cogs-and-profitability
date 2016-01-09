SELECT
	oID,
	tabID,
	dopasPerTab,
	maxInksPerTab,
	totInksPerTab,
	inkCntList,
	`c`.qty AS qtyPerTab,
	stationTypeId,
	tot_imps_per_tab,
	tab_score_reg,
	tab_score_weighted,
	runTime
FROM
	(
		SELECT
			oId AS oID,
			doId AS tabID,
			count(DISTINCT dopaId) AS dopasPerTab,
			max(inksPerDopa) AS maxInksPerTab,
			sum(inksPerDopa) AS totInksPerTab,
			GROUP_CONCAT(inksPerDopa) AS inkCntList
		FROM
			(
				SELECT
					o_id AS oId,
					do_id AS doId,
					dopa_id AS dopaId,
					count(doic_id) AS inksPerDopa
				FROM
					(
						SELECT
							design_order.orderId AS o_id,
							design_order.id do_id,
							designorderinkcolor.designOrderPrintAreaId AS dopa_id,
							designorderinkcolor.id AS doic_id
						FROM
							design_order
						INNER JOIN designorderprintarea ON design_order.id = designorderprintarea.designOrderId
						INNER JOIN designorderinkcolor ON designorderinkcolor.designOrderPrintAreaId = designorderprintarea.id
						WHERE
							printMethodId = 1
					) `a`
				GROUP BY
					`a`.dopa_id
			) `b`
		GROUP BY
			`b`.doId
	) `m`
JOIN (
	SELECT
		`do`.id AS DOID,
		sum(`disdo`.quantity) AS qty
	FROM
		design_order `do`
	JOIN designitemorder dio ON dio.designOrderId = `do`.id
	JOIN designitemsizes_design_order disdo ON disdo.designItemOrderId = dio.id
	GROUP BY
		1
) `c` ON `c`.DOID = `m`.tabID
JOIN `analytics`.v_jobScoreInt ON `analytics`.v_jobScoreInt.orderId = `m`.oID
WHERE
	`analytics`.v_jobScoreInt.tabsPerOrder = 1
GROUP BY
	oID