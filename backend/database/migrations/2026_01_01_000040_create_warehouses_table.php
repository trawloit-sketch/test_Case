<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     * Tabel warehouses — gudang penyimpanan garam
     */
    public function up(): void
    {
        Schema::create('warehouses', function (Blueprint $table) {
            $table->id();
            $table->string('warehouse_code', 20)->unique()->comment('Kode gudang, contoh: WH-SMP-01');
            $table->string('warehouse_name', 150)->comment('Nama gudang');
            $table->string('location', 200)->nullable()->comment('Lokasi / alamat gudang');
            $table->string('city', 100)->nullable()->comment('Kota lokasi gudang');
            $table->boolean('is_active')->default(true)->comment('Status aktif gudang');
            $table->timestamps();

            $table->index('city');
            $table->index('is_active');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('warehouses');
    }
};
