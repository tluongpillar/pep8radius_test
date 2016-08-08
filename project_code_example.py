@patch(insights_summary_controller_prefix + 'crop_zone_controller')
@patch(insights_summary_controller_prefix + 'ResultList')
@patch(insights_summary_controller_prefix + 'filter_by_user')
def test_get_summary_by_crop_zone__returns_crop_zone_summary_when_user_has_access_to_crop_zone(
        patched_filter_by_user,
        patched_result_list,
        patched_crop_zone_controller):
    expected_crop_zone = uuid.uuid4()

    patched_crop_zone_controller.crop_zone_select.return_value = ["CropZone"]

    mock_harvest_stat = _build_mock_harvest_stat(expected_crop_zone)

    patched_result_list.return_value = [mock_harvest_stat]

    expected_summary = [{
        'Keys': {
            'CropZone': expected_crop_zone
        },
        'Date': EXPECTED_HARVEST_DATE,
        'TotalArea': 1,
        'YieldAvg': 1,
        'YieldVar': 0,
        'MoistureAvg': 1,
        'MoistureVar': 0
    }]

    actual_summary = controller.get_summary_by_crop_zone(expected_crop_zone, MagicMock(), MagicMock())

    assert expected_summary == actual_summary

@patch(insights_summary_controller_prefix + 'crop_zone_controller')
def test_get_summary_by_crop_zone__raises_lookup_error_if_crop_zone_doesnt_exist(patched_crop_zone_controller):
    expected_crop_zone = uuid.uuid4()

    patched_crop_zone_controller.crop_zone_select.return_value = []

    with pytest.raises(LookupError) as ex:
        controller.get_summary_by_crop_zone(expected_crop_zone, MagicMock(), MagicMock())
    assert ex
    
@patch(insights_summary_controller_prefix + 'crop_zone_controller')
@patch(insights_summary_controller_prefix + 'filter_by_user')
def test_get_summary_by_crop_zone__raises_lookup_error_if_harvest_stats_do_not_exist(patched_filter_by_user,
                                                                                     patched_crop_zone_controller):
    expected_crop_zone = uuid.uuid4()
    patched_crop_zone_controller.crop_zone_select.return_value = ["CropZoneKey"]

    with pytest.raises(LookupError) as ex:
        controller.get_summary_by_crop_zone(expected_crop_zone, MagicMock(), MagicMock())
    assert ex
