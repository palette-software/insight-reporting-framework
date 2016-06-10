package main

import (
	log "github.com/palette-software/insight-tester/common/logging"
	dbconn "github.com/palette-software/insight-tester/common/db-connector"
	"os"
	"fmt"
)

func main() {
	log.AddTarget(os.Stdout, log.LevelDebug)

	log.Infof("Starting Insight Reporting on version: %v", reporting_version + build_number)

	const config_file_path = "Config.yml"
	config, err := dbconn.ParseConfig(config_file_path)
	if err != nil {
		log.Fatalf("Failed to parse DB connector config file: %v! Error: %v", config_file_path, err)
	}

	defer dbconn.CloseDB()

	dbconnector := config.DbConnector

	//sql_statement := "select * from palette.threadinfo limit 1"
	//sql_statement := "select go_test.get_max_ts('go_test', 'threadinfo');"
	sql_statement := "select count(1) as c, process from palette.threadinfo where ts > now()::date - 2 group by process order by c;"
	//var count int64
	//var hostname string
	//
	//err = dbconnector.Query(sql_statement, func (columns []string) error {
	//	log.Debugf("Count: %d, Process: %s", count, hostname)
	//	return nil
	//}, &count, &hostname)
	//
	//if err != nil {
	//	log.Errorf("Failed to execute query: %v! Error: %v", sql_statement, err)
	//}

	//err = dbconnector.QueryValues(sql_statement, func (columns []string, values []reflect.Value) error {
	//	log.Debugf("Count: %d, Process: %s", values[0].Int(), values[1].String())
	//	return nil
	//})

	if err != nil {
		log.Errorf("Failed to execute query: %v! Error: %v", sql_statement, err)
	}

	err = logDataModelVersion(&dbconnector)
	if err != nil {
		log.Error(err)
	}

	log.Info("Finished Insight Reporting.")
}

func logDataModelVersion(dbconnector *dbconn.DbConnector) error {
	queryDataModelVersion := "select first_value(version_number) over (order by id desc) as model_version from " +
		dbconnector.Schema + ".db_version_meta v limit 1"

	var version_number string

	err := dbconnector.Query(queryDataModelVersion, func (columns []string) error {
		log.Debugf("Data Model version number: %v", version_number)
		return nil
	}, &version_number)

	if err != nil {
		return fmt.Errorf("Failed to get Data Model version! Error: %v", err)
	}
	return nil
}
